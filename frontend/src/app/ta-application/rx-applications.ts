import { RxObject } from 'src/app/rx-object';
import { Application } from './application.model';

export class RxApplications extends RxObject<Application[]> {
  constructor() {
    super();
    this.value = [];
  }
}

export class RxApplication extends RxObject<Application | null> {
  constructor() {
    super();
    this.value = null;
  }
}
