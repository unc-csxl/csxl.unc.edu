/**
 * The TV Component showcases a plethora of useful information for those near the CSXL entrance on the TV.
 *
 * @author WilL Zahrt
 * @copyright 2024
 * @license MIT
 */

import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TvService } from './tv.service';

@Component({
  selector: 'app-tv',
  templateUrl: './tv.component.html',
  styleUrl: './tv.component.css'
})
export class TvComponent {
  public static Route = {
    path: 'signage',
    component: TvComponent
  };
  date: number = Date.now();

  constructor(protected tvService: TvService) {
    this.tvService.getFastData().subscribe((fastTvData) => {
      console.log(fastTvData);
    });

    this.tvService.getSlowData().subscribe((slowTvData) => {
      console.log(slowTvData);
    });
  }
}
