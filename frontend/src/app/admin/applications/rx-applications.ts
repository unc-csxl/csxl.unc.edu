import { RxObject } from 'src/app/rx-object';
import { Application } from './admin-application.model';

export class RxApplication extends RxObject<Application[]> {
  constructor() {
    super();
    this.value = [];
  }

  //   updateApplication(application: Application): void {
  //     this.value = this.value.map((o) =>
  //       o.equipment_id !== checkout.equipment_id ? o : checkout
  //     );
  //     this.notify();
  //   }
}
