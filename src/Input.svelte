<script>
	import { createEventDispatcher } from 'svelte';
	import Selector from './Selector.svelte';

	const dispatch = createEventDispatcher();
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
	let available_times = Array(slots_per_day * 7).fill(false);

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
		let minutes = ":" + (time_slot * (slot % slots_per_hour))
		if(minutes == 0) {
			minutes = ":00"
		}

		let hour = Math.floor(((slot + valid_times[0]) % slots_per_hour) / 4);
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

	function timeblock(){
		for (let i = start_time; i < end_time; i ++) {
			available_times[valid_times[i]] = true;
		}
	}
</script>

<main on:mouseup={() => {dragging = 0;}}>
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
			<div>
				<button on:click={timeblock}>Submit</button>
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
						{#if slot % 2 == 0}
							<td rowspan="2" class="display-times">
								{get_formatted_time_from_slot(slot)}
							</td>
						{/if}
						{#each Array(7) as _, day}
							<td class="slots {available_times[(day * slots_per_day) + slot + valid_times[0]] ? "available" : ""} {(day * slots_per_day) + slot + valid_times[0] == curr_selection ? "selected" : ""} cell-{slot % slots_per_hour}"
								on:mousedown={start_drag((day * slots_per_day) + slot + valid_times[0])}
								on:mouseover={check_drag((day * slots_per_day) + slot + valid_times[0])}
								on:focus={check_drag((day * slots_per_day) + slot + valid_times[0])}>
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

	.slots {
		height: 14px;
	}

	.display-times {
		font-size: 9px;
	}

    .available {
        background-color: #3581B8;
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