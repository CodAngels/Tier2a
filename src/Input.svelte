<script>
	import { createEventDispatcher } from 'svelte';
	import Selector from './Selector.svelte';

	const dispatch = createEventDispatcher();
	const time_slot = 15;
	const slots_per_hour = 60 / time_slot
	const slots_per_day = 24 * slots_per_hour;

	export let valid_times;

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

	function timeblock(val){
		return () => {
			for (let i = start_time; i < end_time+1; i ++) {
				available_times[valid_times[i]] = val;
			}
		}	
	}
</script>

<div class="main" on:mouseup={() => {dragging = 0;}}>
	<h2><center>Meeting Name: CS178 53rd Week Meeting</center></h2>
	<div class="container">
		<div class="time-block">
			<h2>Mark Time Block</h2>
			<div class="block-selectors">
				<div>
					<h4>Start Time</h4>
					<Selector {valid_times} bind:curr_slot={start_time}/>
				</div>
				<p style="margin-top: 160px">to</p>
				<div>
					<h4>End Time</h4>
					<Selector {valid_times} bind:curr_slot={end_time}/>
				</div>
			</div>
			<div class="block-buttons">
				<button style="background-color:#3581B8; color:white" on:click={timeblock(true)}>Mark Available</button>
				<button style="background-color:#F3F8F2" on:click={timeblock(false)}>Mark Unavailable</button>
			</div>
		</div>

		<div class="selector-prompt">
			<div style="margin:2%">
				<h2 style="margin:0">Mark Individual Slots</h2>
				<h5 style="margin:0">Click Button to Toggle</h5>
			</div>
			<div class="selector">
				<Selector {valid_times} bind:curr_slot={curr_slot}/>
				<div>
					<button class="{available_times[curr_selection] ? 'enabled' : 'disabled'}" on:click={() => {available_times[curr_selection] = !available_times[curr_selection];}}>{available_times[curr_selection] ? "Available": "Unavailable"}</button>
				</div>
			</div>
		</div>

		<div class="selected-times">
			<div style="margin:2%">
				<h3 style="margin:0">Time Slots Selected</h3>
				<h5 style="margin:0">(Click / Drag to toggle times in this display)</h5>
			</div>
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
	</div>
	<div class="bottom-buttons">
		<button on:click={finish}>Submit</button>
	</div>
</div>
	
<style>
	.main{
		position: relative;
    	overflow: auto;
		user-select: none;
		text-align: center;
	}

	.container {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: center;
		margin-left: 8%;
	}

	.block-selectors {
		display: flex;
		flex-direction: row;
		gap: 1em;
	}

	.block-buttons {
		margin-left: 10px;
	}

	.block-buttons > button {
		align-items: center;
		justify-content: center;
		margin: 10px;
	}

	.selector-prompt {
		justify-content: center;
        align-items: center;
        width: 40%;
        display: flex;
		flex-direction: column;
    }

	.selector {
		display: flex;
		flex-direction: row;
	}

	.enabled {
        background-color: #3581B8;
		color: white;
        width: 100px;
		margin-top: 93%;
    }

    .disabled {
        background-color: #F3F8F2;
        width: 100px;
		margin-top: 93%;
    }

	.selected-times{
		display: flex;
		flex-direction: column;
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
		border: 3px solid #FCB07E ;
	}

	.bottom-buttons {
		margin-top: 30px;
	}
</style>