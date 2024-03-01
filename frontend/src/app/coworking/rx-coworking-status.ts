import { RxObject } from '../rx-object';
import { CoworkingStatus, Reservation } from './coworking.models';

export class RxCoworkingStatus extends RxObject<CoworkingStatus> {}

export class RxUpcomingReservation extends RxObject<Reservation[]> {}
