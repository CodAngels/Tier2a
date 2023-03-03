<script>
    let up_arrow = "./up_arrow.png";
	let down_arrow = "./down_arrow.png";
	let left_arrow = "./left_arrow.png";
	let right_arrow = "./right_arrow.png";

    export let valid_times;
	export let curr_slot = 0;

	const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    function get_day(slot) {
		return days[Math.floor(slot / 96)];
	}

	function get_hour(slot) {
		let hour = Math.floor((slot % 96) / 4);
		hour = hour > 12 ? hour - 12 : hour;
		if(hour == 0) {
			return 12;
		}
		return hour;
	}

	function get_minute(slot) {
		let minutes = 15 * (slot % 4);
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

<div>
    <div class="day">
        <button on:click={decrement(96)}><img src={left_arrow} alt="Left Arrow"/></button>
        <p class="day-display">{get_day(valid_times[curr_slot])}</p>
        <button on:click={increment(96)}><img src={right_arrow} alt="Right Arrow"/></button>
    </div>
    <p>Available Times</p>
    <div class="time-buttons">
        <button on:click={increment(4)}><img src={up_arrow} alt="Up Arrow"/></button>
        <button on:click={increment(1)}><img src={up_arrow} alt="Up Arrow"/></button>
    </div>
    <p class="time-display">{get_hour(valid_times[curr_slot])}:{get_minute(valid_times[curr_slot])} {(valid_times[curr_slot] % 96) < 48 ? "AM" : "PM"}</p>
    <div class="time-buttons">
        <button on:click={decrement(4)}><img src={down_arrow} alt="Down Arrow"/></button>
        <button on:click={decrement(1)}><img src={down_arrow} alt="Down Arrow"/></button>
    </div>
</div>

<style>
    .day {
        display: flex;
    }

    .time-display {
        font-size: 28px;
        margin: 0;
    }

    .day-display {
        font-size: 28px;
        width: 150px;
        max-width: 150px;
    }

    .time-buttons {
        padding-right: 55px;
    }

    img {
		max-width: 10px;
	}
</style>