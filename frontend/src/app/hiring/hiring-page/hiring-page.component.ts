import {
  CdkDragDrop,
  moveItemInArray,
  transferArrayItem
} from '@angular/cdk/drag-drop';
import { Component } from '@angular/core';

@Component({
  selector: 'app-hiring-page',
  templateUrl: './hiring-page.component.html',
  styleUrl: './hiring-page.component.css'
})
export class HiringPageComponent {
  /** Route for the routing module */
  public static Route = {
    path: '',
    title: 'Hiring',
    component: HiringPageComponent
  };

  notPreferred = ['Student One', 'Student Two', 'Student Three'];
  notProcessed = ['Student Four', 'Student Five', 'Student Six'];
  preferred = ['Student Seven', 'Student Eight', 'Student Nine'];

  drop(event: CdkDragDrop<string[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }
  }
}
