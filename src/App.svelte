<script>
    import Input from './Input.svelte';
    import { getDatabase, ref, set } from "firebase/database";
    import { initializeApp } from "firebase/app";

    const firebaseConfig = {
        apiKey: "AIzaSyDOE-trJSByBUnuiuRpca2E5f0PVvQXYEg",
        authDomain: "cs178-tier-2a.firebaseapp.com",
        projectId: "cs178-tier-2a",
        storageBucket: "cs178-tier-2a.appspot.com",
        messagingSenderId: "644069895841",
        appId: "1:644069895841:web:eb58ab8b3997f793f6cae0",
        measurementId: "G-56LVPNT62M",
        databaseURL: "cs178-tier-2a-default-rtdb.firebaseio.com"
    };

    const app = initializeApp(firebaseConfig);
    const db = getDatabase(app);

    const time_slot = 15;
	const slots_per_hour = 60 / time_slot
	const slots_per_day = 24 * slots_per_hour;

    // There are 96 30 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 335  maps to 11:30 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [];
	// Initialize valid times to be 9 AM to 9 PM
	for(let day = 0; day < 7; day++) {
		for(let slot = 9 * slots_per_hour; slot < 19 * slots_per_hour; slot++) {
			valid_times.push((day * slots_per_day) + slot);
		}
	}

    let started = false;
    let start_time = -1;
    let curr_name = "";

    let submitted_availability = Array(slots_per_day * 7).fill(0)

    function start() {
        started = true;
        start_time = Date.now()
    }

    function finish(event) {
        function pad(n, z) {
            z = z || 2;
            return ('00' + n).slice(-z);
        }

        let time_taken_ms = event.detail.end_time - start_time;
        let time_taken_s = Math.floor(time_taken_ms / 1000)
        let time_taken_m = Math.floor(time_taken_s / 1000)
        let time_taken = pad(time_taken_m) + ":" + pad(time_taken_s % 60) + "." + pad(time_taken_ms % 1000, 3)
        
        let submitted_times = event.detail.times.reduce(function(arr, e, i) {
            if(e) arr.push(i);
            return arr;
            }, []);
        for(let i = 0; i < submitted_times.length; i++) {
            submitted_availability[submitted_times[i]]++;
        }

        set(ref(db, 'submissions/' + curr_name), {
            name: curr_name,
            time_taken: time_taken,
            times: submitted_times
        });

        console.log(curr_name + ',' + time_taken)
        
        curr_name = "";
        started = false;
        start_time = -1;
    }

    function get_slots_in_day() {
		for(let i = 1; i < valid_times.length; i++) {
			if(valid_times[i] - valid_times[i - 1] != 1) {
				return i;
			}
		}
	}

    function get_formatted_time_from_slot(slot) {
		let minutes = (time_slot * (slot % slots_per_hour))
		minutes = minutes == 0 ? ":00" : (":" + minutes)

		let hour = Math.floor(((slot + valid_times[0]) % slots_per_day) / slots_per_hour);
		console.log(slot + " " + hour);
		if(hour > 12) {
			return (hour - 12) + minutes + " PM"
		}
		else if (hour == 0) {
			return "12:00 AM"
		}
		else {
			return hour + minutes + " AM"
		}
	}

    function get_grad(slot) {
        return () => {
            let max_vl = Math.max(submitted_availability)
            let min_vl = Math.min(submitted_availability)
            if(max_vl == 0) {
                return 0;
            }
            let slope = 9 / (max_vl - min_vl);
            return slope * (submitted_availability[slot] - min_vl)
        }
    }
</script>

<main style="backgroundcolor:#EBE9E9">
    {#if started}
        <Input {valid_times} on:submit={finish}/>
    {:else}
        <div style="position:absolute; top:50%; left:50%; margin: -100px 0 0 -120px">
            <p style="font-size:24px">Name:</p>
            <input type="text" bind:value={curr_name}>
            <button on:click={start}>Start</button>
        </div>
        <!-- <div>
            <table>
                <tr>
                    <td></td>
                    <td>Sun</td>
                    <td>Mon</td>
                    <td>Tue</td>
                    <td>Wed</td>
                    <td>Thu</td>
                    <td>Fri</td>
                    <td>Sat</td>
                </tr>
                {#each Array(get_slots_in_day()) as _, slot}
                    <tr>
                        {#if slot % 2 == 0}
                            <td rowspan="2" class="display-times">
                                {get_formatted_time_from_slot(slot)}
                            </td>
                        {/if}
                        {#each Array(7) as _, day}
                            <td class="slots cell-{slot % slots_per_hour} grad-{Math.max(submitted_availability) < 1 ? "0" : Math.floor((9 / Math.max(submitted_availability)) * submitted_availability[(day * slots_per_day) + slot + valid_times[0]])}">
                            </td>
                        {/each}
                    </tr>
                {/each}
            </table>
        </div> -->
    {/if}
</main>

<style>
    table {
		border-collapse: collapse;
	}

	td {
		text-align: center;
		box-sizing: border-box;
        width: 48px;
        height: 28px;
		border: 2px solid black;
		background-color: #F3F8F2;
    }

	.slots {
		height: 14px;
	}

	.display-times {
		font-size: 9px;
	}

    .cell-0 {
		border-bottom: 0;
	}

	.cell-1 {
		border-top: 0;
		border-bottom: 1px solid black;
	}

	.cell-2 {
		border-top: 1px solid black;
		border-bottom: 0;
	}

	.cell-3 {
		border-top: 0;
	}

    .grad-0 {
		background-color: "#f3f8f2";
	}

	.grad-1 {
		background-color: "#deece2";
	}

	.grad-2 {
		background-color: "#c6e0d5";
	}

	.grad-3 {
		background-color: "#add4cb";
	}

	.grad-4 {
		background-color: "#93c8c5";
	}

	.grad-5 {
		background-color: "#79bbc2";
	}

	.grad-6 {
		background-color: "#60aec0";
	}

	.grad-7 {
		background-color: "#4aa0be";
	}

	.grad-8 {
		background-color: "#3a91bc";
	}

	.grad-9 {
		background-color:  "#3581b8";
	}
</style>