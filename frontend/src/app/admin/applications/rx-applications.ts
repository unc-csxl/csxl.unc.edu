import { RxObject } from 'src/app/rx-object';
import { Application } from './admin-application.model';
import { ApplicationComponent } from 'src/app/ta-application/application-home/application-home.component';

export class RxApplications extends RxObject<Application[]> {
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

export class RxApplication extends RxObject<Application | null> {
  constructor() {
    super();
    this.value = null;
  }
}
