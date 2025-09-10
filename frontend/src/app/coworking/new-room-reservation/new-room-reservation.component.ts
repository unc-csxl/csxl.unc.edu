import { Component } from '@angular/core';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { NewRoomReservationService } from './new-room-reservation.service';
import {
  GetRoomAvailabilityResponse,
  GetRoomAvailabilityResponse_Room
} from '../coworking.models';

type SlotSelection = { room: string; slot: string };

@Component({
  selector: 'app-new-room-reservation',
  templateUrl: './new-room-reservation.component.html',
  styleUrl: './new-room-reservation.component.css',
  standalone: false
})
export class NewRoomReservationComponent {
  public static Route = {
    path: 'new-reservation',
    title: 'New Reservation',
    component: NewRoomReservationComponent,
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  availability: GetRoomAvailabilityResponse | undefined = undefined;

  selectedSlots: SlotSelection[] = [];

  constructor(private roomReservationService: NewRoomReservationService) {
    this.roomReservationService.getAvailability().subscribe((result) => {
      this.availability = result;
    });
  }

  selectSlot(room: GetRoomAvailabilityResponse_Room, slot: string) {
    // Validation
    if (!this.availability) {
      return;
    }
    // First, make sure that the slot is selectable.
    if (room.availability[slot].state !== 'AVAILABLE') {
      return;
    }

    // If there are no existing selections, select the slot.
    if (this.selectedSlots.length === 0) {
      this.selectedSlots.push({ room: room.room, slot });
      return;
    }

    // If existing slots are for a different room, clear the selection and select.
    if (this.selectedSlots[0].room !== room.room) {
      this.selectedSlots = [{ room: room.room, slot }];
      return;
    }

    // For later functionality, get the indexes of the selected slots within the
    // list of slot labels.
    const selectedSlotIndexes = Array.from(this.selectedSlots).map(
      (selectedSlot) => {
        return this.availability!.slot_labels.indexOf(selectedSlot.slot);
      }
    );
    const earliestSlotIndex = Math.min(...selectedSlotIndexes);
    const latestSlotIndex = Math.max(...selectedSlotIndexes);

    const clickedSlotIndex = this.availability!.slot_labels.indexOf(slot);

    // If the clicked slot is already selected:
    //    - If the slot is at the start or end, remove just the slot
    //    - Otherwise, start over selection
    console.log(this.selectedSlots);
    if (
      this.selectedSlots.find((v) => v.room === room.room && v.slot === slot)
    ) {
      if (
        clickedSlotIndex === earliestSlotIndex ||
        clickedSlotIndex === latestSlotIndex
      ) {
        this.selectedSlots = this.selectedSlots.filter(
          (v) => v.room !== room.room || v.slot !== slot
        );
        return;
      } else {
        this.selectedSlots = [{ room: room.room, slot }];
        return;
      }
    }

    // Otherwise, if a slot is before the earliest selection, we start over at
    // the new selection
    if (clickedSlotIndex < earliestSlotIndex) {
      this.selectedSlots = [{ room: room.room, slot }];
      return;
    }

    // Otherwise, the final case is that the clicked slot is some time after the
    // currently selected range. We want to either:
    // 1. Restart the range if there is an interruption of available slots for the room between
    //    the start and the end of the range, or:
    // 2. Fill in the range up to the selected date.
    let isInterruption: boolean = false;
    let currentIndex = latestSlotIndex + 1;
    let slotsToAdd: SlotSelection[] = [];
    while (currentIndex <= clickedSlotIndex) {
      if (
        room.availability[this.availability.slot_labels[currentIndex]].state !==
        'AVAILABLE'
      ) {
        isInterruption = true;
      }
      slotsToAdd.push({
        room: room.room,
        slot: this.availability.slot_labels[currentIndex]
      });
      currentIndex += 1;
    }

    if (isInterruption) {
      this.selectedSlots = [{ room: room.room, slot }];
      return;
    } else {
      slotsToAdd.forEach((slot) => this.selectedSlots.push(slot));
      return;
    }
  }

  isSlotSelected(room: GetRoomAvailabilityResponse_Room, slot: string) {
    return !!this.selectedSlots.find(
      (v) => v.room === room.room && v.slot === slot
    );
  }

  clearSelections() {
    this.selectedSlots = [];
  }

  printSelected() {
    console.log(this.selectedSlots);
  }
}
