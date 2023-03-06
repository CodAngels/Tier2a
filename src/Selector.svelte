<script>
    export let valid_times;
	export let curr_slot = 0;

	const time_slot = 15;
	const slots_per_hour = 60 / time_slot
	const slots_per_day = 24 * slots_per_hour;

	const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

	function get_slots_in_day() {
		for(let i = 1; i < valid_times.length; i++) {
			if(valid_times[i] - valid_times[i - 1] != 1) {
				return i;
			}
		}
	}

    function get_day(slot) {
		return days[Math.floor(slot / slots_per_day)];
	}

	function get_hour(slot) {
		let hour = Math.floor((slot % slots_per_day) / slots_per_hour);
		hour = hour > 12 ? hour - 12 : hour;
		if(hour == 0) {
			return 12;
		}
		return hour;
	}

	function get_minute(slot) {
		let minutes = time_slot * (slot % slots_per_hour);
		return minutes == 0 ? "00" : minutes;
	}

	function increment(delta) {
		return function() {
			curr_slot += delta;
			if(curr_slot >= valid_times.length) {
				curr_slot -= valid_times.length;
			}
		}
	}

	function decrement(delta) {
		return function() {
			curr_slot -= delta;
			if(curr_slot < 0) {
				curr_slot += valid_times.length;
			}
		}
	}
</script>

<div class="daytime-picker">
    <div class="day-picker">
        <button on:click={decrement(get_slots_in_day())}>←</button>
        <span class="day-display">{get_day(valid_times[curr_slot])}</span>
        <button on:click={increment(get_slots_in_day())}>→</button>
    </div>
	<div class="time-picker">
		<div class="hour-picker">
			<button on:click={increment(slots_per_hour)}>↑</button>
			<span>{get_hour(valid_times[curr_slot])}</span>
			<button on:click={decrement(slots_per_hour)}>↓</button>
		</div>
		<span>:</span>
		<div class="minute-picker">
			<button on:click={increment(1)}>↑</button>
			<span>{get_minute(valid_times[curr_slot])}</span>
			<button on:click={decrement(1)}>↓</button>
		</div>
		<span>{(valid_times[curr_slot] % slots_per_day) < (slots_per_day / 2) ? " AM" : " PM"}</span>
	</div>
</div>

<style>
 	.daytime-picker {
    	display: flex;
		flex-direction: column;
    	align-items: center;
    	gap: 1rem;
  	}

	.time-picker {
		display: flex;
    	align-items: center;
		margin-left: 20px;
	}

  	.hour-picker,
  	.minute-picker {
    	display: flex;
    	flex-direction: column;
    	align-items: center;
    	gap: 0.5rem;
  	}

	.day-display {
		display: inline-block;
		width: 85px;
		max-width: 85px;
	}

  	button {
		font-size: 1rem;
		padding: 0.25rem 0.5rem;
		border-radius: 0.25rem;
		border: 1px solid #ccc;
		background-color: white;
		cursor: pointer;
  	}

	button:focus {
		outline: none;
	}
</style>