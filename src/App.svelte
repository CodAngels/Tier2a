<script>
    import Input from './Input.svelte';

    let started = false;
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
        let submitted_times = event.detail.times;

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