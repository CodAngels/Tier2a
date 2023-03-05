<script>
	import Selector from './Selector.svelte';

	// There are 96 30 minute blocks in a day. There are 96 * 7 = 672 blocks in a week. 0 maps to 12:00 AM on Sunday, 671 maps to 11:45 PM on Saturday
	// This array gives the number of blocks that are available to be booked (default is the entire week)
	let valid_times = [];
	// Initialize valid times to be 9 AM to 9 PM
	for(let day = 0; day < 7; day++) {
		for(let slot = 18; slot < 44; slot++) {
			valid_times.push((day * 48) + slot);
		}
	}
	let available_times = Array(336).fill(false);

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
		<div>
			<h3>Mark Available Block</h3>
			<div>
				<p>Start Time</p>
				<Selector {valid_times} bind:curr_slot={curr_slot}/>
			</div>
			<div>
				<p>End Time</p>
				<Selector {valid_times} bind:curr_slot={curr_slot}/>
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
					{#each Array(7) as _, day}
						<td class={available_times[(day * 48) + slot + valid_times[0]] ? "available cell-" + (slot % 2) : "unavailable cell-" + (slot % 2)}>
							<div style="width: 100%; height: 100%">
								<button class="slot-toggle" on:click={() => {available_times[(day * 48) + slot + valid_times[0]] = !available_times[(day * 48) + slot + valid_times[0]];}}></button>
							</div>
						</td>
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
        width: 35px;
        height: 19px;
		border: 2px solid black;
    }

    .available {
        background-color: green;
    }

    .unavailable {
        background-color: antiquewhite;
    }

	.cell-0 {
		border-bottom: 1px solid black;
	}

	.cell-1 {
		border-top: 1px solid black;
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