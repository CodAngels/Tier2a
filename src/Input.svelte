<script>
	import { createEventDispatcher } from 'svelte';
	import Selector from './Selector.svelte';

	const dispatch = createEventDispatcher();

	// There are 96 30 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 335  maps to 11:30 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [];
	// Initialize valid times to be 9 AM to 9 PM
	for(let day = 0; day < 7; day++) {
		for(let slot = 18; slot < 38; slot++) {
			valid_times.push((day * 48) + slot);
		}
	}
	let available_times = Array(336).fill(false);

	let curr_slot = 0;
	$: curr_selection = valid_times[curr_slot]

	let start_time = 0;
	let end_time = 0;

	let dragging = 0;

	function get_slots_in_day() {
		for(let i = 1; i < valid_times.length; i++) {
			if(valid_times[i] - valid_times[i - 1] != 1) {
				return i;
			}
		}
	}

	function finish() {
		dispatch('submit', {
			times: available_times,
			end_time: Date.now()
		})
	}

	function start_drag(slot) {
		return () => {
			curr_slot = valid_times.indexOf(slot);
			available_times[slot] = !available_times[slot];
			if(available_times[slot]) {
				dragging = 1;
			}
			else {
				dragging = 2;
			}
		}
	}

	function check_drag(slot) {
		return () => {
			if(dragging != 0) {
				curr_slot = valid_times.indexOf(slot);
				available_times[slot] = dragging == 1;
			}
		}
	}

	function get_formatted_time_from_slot(slot) {
		let hour = Math.floor(((slot + valid_times[0]) % 48) / 2);
		let minutes = slot % 2 ? ":00" : ":30"
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

<main>
	<div class="container">
		<h2><center>Meeting Name: CS178 53rd Week Meeting</center></h2>
		<div>
			<h3>Mark Available Block</h3>
			<div>
				<p>Start Time</p>
				{start_time}
				<Selector {valid_times} bind:curr_slot={start_time}/>
			</div>
			<div>
				<p>End Time</p>
				{end_time}
				<Selector {valid_times} bind:curr_slot={end_time}/>
			</div>
		</div>
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
						<td class="display-times">
							{get_formatted_time_from_slot(slot)}
						</td>
						{#each Array(7) as _, day}
							<td class="{available_times[(day * 48) + slot + valid_times[0]] ? "available" : ""} {(day * 48) + slot + valid_times[0] == curr_selection ? "selected" : ""} {slot % 2}"
								on:mousedown={start_drag((day * 48) + slot + valid_times[0])}
								on:mouseover={check_drag((day * 48) + slot + valid_times[0])}
								on:focus={check_drag((day * 48) + slot + valid_times[0])}
								on:mouseup={() => {dragging = 0;}}>
							</td>
						{/each}
					</tr>
				{/each}
			</table>
		</div>

		<div class="bottom-buttons">
			<button class="submit" on:click={finish}>Submit</button>
			<button class="share">Share</button>
		</div>
			
	</div>
</main>
	
<style>
	.container{
		background-color: #EBE9E9;
		position: relative;
    	overflow: auto;
		user-select: none;
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
        background-color: #3581B8;
		color: white;
        width: 100px;
    }

    .disabled {
        background-color: #F3F8F2;
        width: 100px;
    }

	.slot-toggle,
	.slot-toggle:focus {
		background-color: transparent;
		border: 0;
		margin: 0;
		padding: 0;
		width: 100%;
		height: 100%;
		border-radius: 0;
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

	.display-times {
		font-size: 9px;
	}

    .available {
        background-color: #3581B8;
    }

	.cell-0 {
		border-bottom: 1px solid black;
	}

	.cell-1 {
		border-top: 1px solid black;
	}

	.selected {
		position: relative;
		border: 3px solid #FCB07E ;
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