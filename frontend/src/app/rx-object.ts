/**
 * Abstract base class for "Reactive Objects", an XL App pattern for interactive objects. 
 * These objects are typically models whose data is loaded from the backend API and whose
 * state is mutable via user interactions with the object.
 * 
 * Extended classes add methods to update the object `value`, or properties of it,
 * and call the `notify()` method which pushes an update to all `value$` subscribers.
 * By design, set and the `value$` observable are only publicly exposed members of `RxObject`.
 * 
 * For subclass implementers, the general strategy is to treat the protected member `value`
 * as the most recent value of the object, mutate it or replace it as necessary during 
 * an implemented method's operation, and then **be sure to call notify()* so that dependent
 * subscribers to this object (typically views/UI) are updated to reflect.
 * 
 * @author Kris Jordan <kris@cs.unc.edu>
 */

import { Observable, ReplaySubject, Subject } from "rxjs";

export abstract class RxObject<T> {

    /**
     * The last/most recent value of the RxObject.
     */
    protected value!: T;

    /**
     * The Subject provides a "multicast" mechanism for publishing changes to observers.
     * We choose a ReplaySubject with a value of 1 such that every new observer is guaranteed
     * to receive the latest value immediately upon observation, once an initial value has
     * been set.
     */
    private subject: Subject<T> = new ReplaySubject(1);

    /**
     * This exposed Observable is what all Components and Services dependent on the RxObject
     * are expected to subscribe to for updates and changes of state to the object. 
     */
    public value$: Observable<T> = this.subject.asObservable();

    /**
     * Replace the last value of the RxObject with a new value and notify observers.
     *  
     * @param value The new value of the RxObject.
     */
    set(value: T): void {
        this.value = value;
        this.notify();
    }

    /**
     * Subclasses are expected to make mutable changes to `this.value` and then call `this.notify()`
     * in order to broadcast changes to all dependent subscribers of this RxObject.
     */
    protected notify() {
        this.subject.next(this.value);
    }

}