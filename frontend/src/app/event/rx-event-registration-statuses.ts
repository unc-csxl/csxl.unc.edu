import { RxObject } from '../rx-object';
import { UserRegistrationStatus } from './event.model';

export class RxEventRegistrationStatuses extends RxObject<
  UserRegistrationStatus[]
> {
  register(event_id: number): void {
    this.value = this.value.map((o) => {
      if (o.event_id == event_id) {
        o.is_registered = true;
      }
      return o;
    });

    this.notify();
  }

  unregister(event_id: number): void {
    this.value = this.value.map((o) => {
      if (o.event_id == event_id) {
        o.is_registered = false;
      }
      return o;
    });

    this.notify();
  }
}
