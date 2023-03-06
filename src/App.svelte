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

    let started = true;
    let start_time = -1;
    let curr_name = "";

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
</script>

{#if started}
    <Input on:submit={finish}/>
{:else}
    <main>
        <div>
            <p>Name:</p>
            <input type="text" bind:value={curr_name}>
            <button on:click={start}>Start</button>
        </div>
    </main>
{/if}