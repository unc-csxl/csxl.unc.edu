/**
 * The Room Lookup Widget allows users to search for a room
 * from a preloaded list.
 */

import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
  ViewChild
} from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { Observable, map, startWith } from 'rxjs';
import { Room } from 'src/app/academics/academics.models';

@Component({
  selector: 'room-lookup',
  templateUrl: './room-lookup.widget.html',
  styleUrls: ['./room-lookup.widget.css'],
  standalone: false
})
export class RoomLookup {
  @Input() label: string = 'Room';
  @Input() rooms: Room[] = [];
  @Input() disabled: boolean | null = false;

  private _selectedRoom: Room | null = null;

  @Input() set selectedRoom(room: Room | null) {
    this._selectedRoom = room;
    if (!room) {
      this.roomLookup.setValue('', { emitEvent: false });
    }
  }

  get selectedRoom(): Room | null {
    return this._selectedRoom;
  }

  @Output() selectedRoomChange: EventEmitter<Room | null> = new EventEmitter();

  public roomLookup = new FormControl<string | Room>('');
  public filteredRooms$: Observable<Room[]> = this.roomLookup.valueChanges.pipe(
    startWith(''),
    map((value) => this.filterRooms(this.displayRoom(value)))
  );

  @ViewChild('roomInput') roomInput?: ElementRef<HTMLInputElement>;

  onRoomAdded(event: MatAutocompleteSelectedEvent): void {
    const room = event.option.value as Room;
    this.clearLookup();
    this.selectedRoomChange.emit(room);
  }

  onRoomRemoved(): void {
    this.clearLookup();
    this.selectedRoomChange.emit(null);
  }

  displayRoom = (room: Room | string | null): string => {
    if (!room) {
      return '';
    }

    if (typeof room === 'string') {
      return room;
    }

    const location = [room.building, room.room].filter(Boolean).join(' ');
    return location ? `${room.nickname} (${location})` : room.nickname;
  };

  private clearLookup(): void {
    if (this.roomInput) {
      this.roomInput.nativeElement.value = '';
    }

    this.roomLookup.setValue('', { emitEvent: false });
  }

  private filterRooms(search: string): Room[] {
    const normalizedSearch = search.trim().toLowerCase();
    const selectableRooms = this.rooms.filter(
      (room) => room.id !== this.selectedRoom?.id
    );

    if (!normalizedSearch) {
      return selectableRooms;
    }

    return selectableRooms.filter((room) =>
      [room.nickname, room.building, room.room]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
        .includes(normalizedSearch)
    );
  }
}
