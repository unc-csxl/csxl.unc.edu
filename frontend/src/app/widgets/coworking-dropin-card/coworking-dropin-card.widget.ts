import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { Seat, SeatAvailability } from 'src/app/coworking/coworking.models';

class SeatCategory {
    public title: string;

    public reservable_now: boolean = false;
    public seats_available_now: SeatAvailability[] = []

    public reservable_soon: boolean = false;
    public next_available?: SeatAvailability;
    public seats_available_soon: SeatAvailability[] = []

    // TODO: Handle edge case where only openings are < 1hr
    // public truncated: boolean = false;
    // public truncated_at?: Date;

    constructor(title: string) {
        this.title = title;
    }

    push(seat: SeatAvailability) {
        let now = new Date()
        if (seat.availability[0].start <= now) {
            this.seats_available_now.push(seat);
            if (this.seats_available_now.length === 1) {
                this.reservable_now = true;
                this.next_available = seat;
            }
        } else {
            this.seats_available_soon.push(seat);
            if (!this.reservable_now && this.seats_available_soon.length === 1) {
                this.reservable_soon = true;
                this.next_available = seat;
            }
        }
    }

    availabilityString(): string {
        let result = "Available ";
        if (this.reservable_now) {
            result += "now";
        } else if (this.reservable_soon) {
            result += " in ";
            let now = new Date();
            let start = this.seats_available_soon[0].availability[0].start;
            let delta = Math.ceil((start.getMilliseconds() - now.getMilliseconds()) / (60 * 1000));
            result += ` ${delta} minutes`;
        } else {
            return "None available";
        }
        return result;
    }
}

const MONITOR_SITTING = 0;
const MONITOR_STANDING = 1;
const COMMON_AREA = 2;

@Component({
    selector: 'coworking-dropin-card',
    templateUrl: './coworking-dropin-card.widget.html',
    styleUrls: ['./coworking-dropin-card.widget.css']
})
export class CoworkingDropInCard implements OnChanges {

    @Input() seat_availability!: SeatAvailability[];
    @Output() onSeatsSelected = new EventEmitter<SeatAvailability[]>();

    public categories: SeatCategory[];

    constructor() {
        this.categories = this.initCategories();
    }

    ngOnChanges(changes: SimpleChanges): void {
        this.seat_availability = changes['seat_availability'].currentValue;
        this.categories = this.initCategories();
        for (let seat of this.seat_availability) {
            if (seat.has_monitor) {
                if (seat.sit_stand) {
                    this.categories[MONITOR_STANDING].push(seat);
                } else {
                    this.categories[MONITOR_SITTING].push(seat);
                }
            } else {
                this.categories[COMMON_AREA].push(seat);
            }
        }
    }

    reserve(category: SeatCategory): void {
        this.onSeatsSelected.emit([...category.seats_available_now, ...category.seats_available_soon]);
    }

    private initCategories(): SeatCategory[] {
        return [
            new SeatCategory("Monitor Desk (Sitting)"),
            new SeatCategory("Monitor Desk (Sit or Stand)"),
            new SeatCategory("Common Area"),
        ];
    }

}
