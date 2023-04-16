<script>
    import Input from './Input.svelte';
    import { getDatabase, ref, set, get } from "firebase/database";
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

    // There are 96 15 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 335  maps to 11:30 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [];
	// Initialize valid times to be 9 AM to 7 PM
	for(let day = 0; day < 7; day++) {
		for(let slot = 9 * slots_per_hour; slot < 19 * slots_per_hour; slot++) {
			valid_times.push((day * slots_per_day) + slot);
		}
	}

    let started = false;
    let start_time = -1;
    let curr_name = "";

    // TIMESLOT CONCEPT, submitted availability keeps track of the cumulative number of available users for each time slot
    let submitted_availability = fill_availability();

    function fill_availability() {
        let avail = Array(slots_per_day * 7).fill(0);
        get(ref(db, 'submissions')).then((data) => {
            for(var key in data.val()) {
                let times = data.val()[key]["times"]
                for(let i = 0; i < times.length; i++) {
                    submitted_availability[times[i]]++;
                }
            }
        })
        return avail
    }

    function start() {
        started = true;
        start_time = Date.now()
        // USER CONCEPT, curr_name representing the username of the current logged-in user
        if(curr_name == "") {
            curr_name = "empty"
        }
    }

    function finish(event) { 
        let submitted_times = event.detail.times.reduce(function(arr, e, i) {
            if(e) arr.push(i);
            return arr;
            }, []);

        set(ref(db, 'submissions/' + curr_name), {
            name: curr_name,
            start_time: start_time,
            end_time: event.detail.end_time,
            times: submitted_times
        });

        fill_availability()
        console.log(curr_name + "," + start_time + "," + event.detail.end_time + "," + (event.detail.end_time-start_time))
        
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
</script>

<main style="backgroundcolor:#EBE9E9">
    {#if started}
        <Input {valid_times} on:submit={finish}/>
    {:else}
    <div class="container">
        <div>
            <p style="font-size:24px">Name:</p>
            <input type="text" bind:value={curr_name}>
            <button on:click={start}>Start</button>
        </div>
        <div style="text-align:center">
            <h5>Heatmap of Times Selected By All Respondents</h5>
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
                            <td class="slots cell-{slot % slots_per_hour} 
                                grad-{Math.max(...submitted_availability) < 1 ? "0" : Math.floor((9 / Math.max(...submitted_availability)) * submitted_availability[(day * slots_per_day) + slot + valid_times[0]])}">
                            </td>
                        {/each}
                    </tr>
                {/each}
            </table>
        </div>
    </div>
    {/if}
</main>

<style>
    .container {
        display:flex; 
        flex-direction:row;
        justify-content: center;
        align-items: center;
        gap: 200px;
    }

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
		background-color: #f3f8f2;
	}

	.grad-1 {
		background-color: #deece2;
	}

	.grad-2 {
		background-color: #c6e0d5;
	}

	.grad-3 {
		background-color: #add4cb;
	}

	.grad-4 {
		background-color: #93c8c5;
	}

	.grad-5 {
		background-color: #79bbc2;
	}

	.grad-6 {
		background-color: #60aec0;
	}

	.grad-7 {
		background-color: #4aa0be;
	}

	.grad-8 {
        background-color: #3A91BC;
	}

	.grad-9 {
		background-color: #3581B8;
	}
</style>