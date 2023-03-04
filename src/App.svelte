<script>
	import Selector from './Selector.svelte';

	// There are 96 15 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 671 maps to 11:45 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [...Array(672).keys()];
	let available_times = Array(672).fill(false);

	let curr_slot = 0;
	$: curr_selection = available_times[curr_slot]

	function toggle_curr() {
		curr_selection = !curr_selection;
		available_times[curr_slot] = curr_selection;
	}

	let start_time = 0;
	let end_time = 0;
</script>

<main>
	<div class="container">
		<h2><center>Meeting Name: CS178 53rd Week Meeting</center></h2>
		<!-- <div>
			<p>Add Conflicting Event</p>
			<div>
				<p>Start Time</p>
				<Selector {valid_times} bind:start_time={curr_slot}/>
			</div>
			<div>
				<p>End Time</p>
				<Selector {valid_times} bind:end_time={curr_slot}/>
			</div>
		</div> -->
		<h3 class="select-prompt">Select Availability</h3>

		<div class="selector">
			<Selector {valid_times} bind:curr_slot={curr_slot}/>
			<div>
				<button class="{curr_selection ? 'enabled' : 'disabled'}" on:click={toggle_curr}>{curr_selection ? "Available": "Unavailable"}</button>
			</div>
		</div>

		<h3 class="TimeSlot">Time Slots Selected</h3>
		<div class="selectedTimes">
			<!-- Doesn't work right now, but probably want to use a different approach anyway so not spending more time debugging -->
			{#each valid_times as time}
				{#if available_times[valid_times] == true}
					<div key={time}>{time}
						<button on:click={() => available_times[valid_times] = false}>Delete</button>
					</div>
				{/if}
			{/each}
		</div>

		<div class="bottom-buttons">
			<button class="submit">Submit</button>
			<button class="share">Share</button>
		</div>
			
	</div>
</main>

<style>
	.container{
		position: relative;
    	overflow: auto;
	}

	.select-prompt {
		position: relative;
  		bottom: 100;
  		left: 20%;
  		margin: 25px;
		overflow-y: auto;
	}

	.selector {
        justify-content: center;
        width: 100%;
        display: flex;
        padding-top: 240px;
    }

	.enabled {
        background-color: green;
        width: 100px;
    }

    .disabled {
        background-color: red;
        width: 100px;
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
</style>