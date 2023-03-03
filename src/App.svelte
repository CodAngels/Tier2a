<script>
	export let up_arrow = "./up_arrow.png";
	export let down_arrow = "./down_arrow.png";
	export let left_arrow = "./left_arrow.png";
	export let right_arrow = "./right_arrow.png";

	// There are 96 15 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 671 maps to 11:45 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	export let valid_times = [...Array(672).keys()];
	export let available_times = Array(672).fill(false);
	export let curr_slot = 0;

	export let curr_selection = false;

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
			curr_selection = available_times[curr_slot];
		}
	}

	function decrement(delta) {
		return function() {
			curr_slot -= delta;
			if(curr_slot < 0) {
				curr_slot += valid_times.length;
			}
			curr_selection = available_times[curr_slot];
		}
	}

	function toggle_curr() {
		curr_selection = !curr_selection;
		available_times[curr_slot] = curr_selection;
	}
</script>

<main>
	<div class="selector">
		<div>
			<div class="day">
				<button on:click={decrement(96)}><img src={left_arrow} alt="Left Arrow"/></button>
				<p class="time-display">{get_day(valid_times[curr_slot])}</p>
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
		<div>
			<button class="{curr_selection ? 'enabled' : 'disabled'}" on:click={toggle_curr}>{curr_selection ? "Available": "Unavailable"}</button>
		</div>
	</div>

	<div class="bottom-buttons">
		<button class="submit">Submit</button>
		<button class="share">Share</button>
	</div>
	
</main>

<style>
	main {
		text-align: center;
	}

	.selector {
		justify-content: center;
		width: 100%;
		display: flex;
		padding-top: 240px;
	}

	.day {
		display:flex;
	}

	.time-display {
		margin: 0;
	}

	.time-buttons {
		padding-right: 50px;
	}

	.enabled {
		background-color: green;
		margin-left: 2px;
		margin-top: 132px;
	}

	.disabled {
		background-color: red;
		margin-left: 2px;
		margin-top: 132px;
	}

	.bottom-buttons {
		padding-top: 100px;
		width: 80%;
	}

	.submit {
		float: center;
	}

	.share {
		float: right;
	}

	.time-display {
		font-size: 28px;
	}

	img {
		max-width: 10px;
	}
</style>