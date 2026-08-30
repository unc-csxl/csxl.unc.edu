import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, signal } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Route } from '@angular/router';
import { Room } from 'src/app/academics/academics.models';
import { AcademicsService } from 'src/app/academics/academics.service';
import { permissionGuard } from 'src/app/permission.guard';
import {
  NewRoomReservationBlock,
  RoomReservationBlock
} from '../coworking.models';
import { RoomReservationBlockService } from '../room-reservation-block.service';

@Component({
  selector: 'app-room-reservation-block-admin',
  templateUrl: './room-reservation-block-admin.component.html',
  standalone: false
})
export class RoomReservationBlockAdminComponent implements OnInit {
  static readonly Route: Route = {
    path: 'admin/room-reservation-blocks',
    title: 'Standing Room Reservations',
    component: RoomReservationBlockAdminComponent,
    canActivate: [
      permissionGuard('coworking.room_reservation_blocks.read', 'room/*')
    ]
  };

  readonly weekdays = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  ];
  readonly blocks = signal<RoomReservationBlock[]>([]);
  readonly rooms = signal<Room[]>([]);
  readonly editingId = signal<number | null>(null);

  readonly form = this.formBuilder.nonNullable.group({
    room_id: ['', Validators.required],
    label: ['', [Validators.required, Validators.maxLength(120)]],
    weekday: [0, [Validators.required, Validators.min(0), Validators.max(6)]],
    start_time: ['09:00', Validators.required],
    end_time: ['10:00', Validators.required],
    starts_on: [this.today(), Validators.required],
    ends_on: [''],
    enabled: [true]
  });

  constructor(
    private formBuilder: FormBuilder,
    private blockService: RoomReservationBlockService,
    private academicsService: AcademicsService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadBlocks();
    this.academicsService.getRooms().subscribe({
      next: (rooms) => this.rooms.set(rooms.filter((room) => room.reservable)),
      error: () => this.showError('Unable to load rooms.')
    });
  }

  save(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.getRawValue();
    const request: NewRoomReservationBlock = {
      ...value,
      ends_on: value.ends_on || null
    };
    const id = this.editingId();
    const operation =
      id === null
        ? this.blockService.create(request)
        : this.blockService.update(id, request);

    operation.subscribe({
      next: () => {
        this.snackBar.open(
          id === null ? 'Block created.' : 'Block updated.',
          '',
          { duration: 2000 }
        );
        this.cancelEdit();
        this.loadBlocks();
      },
      error: (error: HttpErrorResponse) =>
        this.showError(error.error?.message ?? 'Unable to save block.')
    });
  }

  edit(block: RoomReservationBlock): void {
    this.editingId.set(block.id);
    this.form.setValue({
      room_id: block.room_id,
      label: block.label,
      weekday: block.weekday,
      start_time: block.start_time.slice(0, 5),
      end_time: block.end_time.slice(0, 5),
      starts_on: block.starts_on,
      ends_on: block.ends_on ?? '',
      enabled: block.enabled
    });
  }

  cancelEdit(): void {
    this.editingId.set(null);
    this.form.reset({
      room_id: '',
      label: '',
      weekday: 0,
      start_time: '09:00',
      end_time: '10:00',
      starts_on: this.today(),
      ends_on: '',
      enabled: true
    });
  }

  delete(block: RoomReservationBlock, event: Event): void {
    event.stopPropagation();
    const confirmation = this.snackBar.open(
      `Delete “${block.label}” from ${block.room_id}?`,
      'Delete'
    );
    confirmation.onAction().subscribe(() => {
      this.blockService.delete(block.id).subscribe({
        next: () => {
          if (this.editingId() === block.id) {
            this.cancelEdit();
          }
          this.loadBlocks();
          this.snackBar.open('Block deleted.', '', { duration: 2000 });
        },
        error: (error: HttpErrorResponse) =>
          this.showError(error.error?.message ?? 'Unable to delete block.')
      });
    });
  }

  private loadBlocks(): void {
    this.blockService.list().subscribe({
      next: (blocks) => this.blocks.set(blocks),
      error: () => this.showError('Unable to load standing reservations.')
    });
  }

  private showError(message: string): void {
    this.snackBar.open(message, 'Close', { duration: 8000 });
  }

  private today(): string {
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${now.getFullYear()}-${month}-${day}`;
  }
}
