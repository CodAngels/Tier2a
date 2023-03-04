<script>
	import Selector from './Selector.svelte';

	// There are 96 15 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 671 maps to 11:45 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [];
	// Initialize valid times to be 9 AM to 9 PM
	for(let day = 0; day < 7; day++) {
		for(let slot = 36; slot < 88; slot++) {
			valid_times.push((day * 96) + slot);
		}
	}
	let available_times = Array(672).fill(false);

	let curr_slot = 0;
	$: curr_selection = valid_times[curr_slot]

	let start_time = 0;
	let end_time = 0;

	function get_slots_in_day() {
		for(let i = 1; i < valid_times.length; i++) {
			if(valid_times[i] - valid_times[i - 1] != 1) {
				return i;
			}
		}
	}
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
				<button class="{available_times[curr_selection] ? 'enabled' : 'disabled'}" on:click={() => {available_times[curr_selection] = !available_times[curr_selection];}}>{available_times[curr_selection] ? "Available": "Unavailable"}</button>
			</div>
		</div>

		<h3 class="TimeSlot">Time Slots Selected</h3>
		<div class="selectedTimes">
			<table>
				<tr>
					<td>Sun</td>
					<td>Mon</td>
					<td>Tue</td>
					<td>Wed</td>
					<td>Thu</td>
					<td>Fri</td>
					<td>Sat</td>
				</tr>
				{#each [...Array(get_slots_in_day()).keys()] as slot}
					<tr>
					{#each [...Array(7).keys()] as day}
						<td class={available_times[(day * get_slots_in_day()) + slot + valid_times[0]] ? "available cell-" + (slot % 4) : "unavailable cell-" + (slot % 4)}></td>
					{/each}
					</tr>
				{/each}
			</table>
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

	table {
		border-collapse: collapse;
	}

	td {
		text-align: center;
        width: 35px;
        height: 6px;
		border-collapse: 0;
		border: 2px solid black;
    }

    .available {
        background-color: green;
    }

    .unavailable {
        background-color: antiquewhite;
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