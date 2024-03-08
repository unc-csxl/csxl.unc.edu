/**
 * @author Kris Jordan, John Schachte
 * @copyright 2023
 * @license MIT
 */

import { RxObject } from '../rx-object';
import { CoworkingStatus, Reservation } from './coworking.models';

export class RxCoworkingStatus extends RxObject<CoworkingStatus> {}

export class RxUpcomingReservation extends RxObject<Reservation[]> {}
