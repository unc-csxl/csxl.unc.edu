/**
 * The TV Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author WilL Zahrt
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SignageService } from './signage.service';

@Component({
  selector: 'app-signage',
  templateUrl: './signage.component.html',
  styleUrl: './signage.component.css'
})
export class SignageComponent {
  public static Route = {
    path: 'signage',
    component: SignageComponent
  };
  date: number = Date.now();

  constructor(protected signageService: SignageService) {
    this.signageService.getFastData().subscribe((fastSignageData) => {
      console.log(fastSignageData);
    });

    this.signageService.getSlowData().subscribe((slowSignageData) => {
      console.log(slowSignageData);
    });
  }
}
