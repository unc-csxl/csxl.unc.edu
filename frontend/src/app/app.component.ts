import { Component, OnInit } from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Observable, filter } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  title = 'frontend';
  childRoute: string = '';

  constructor(
    private matIconReg: MatIconRegistry,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.matIconReg.setDefaultFontSetClass('material-symbols-outlined');

    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe(() => {
        // When the route navigation is completed, get the child
        this.childRoute =
          this.route.firstChild?.snapshot.url[0]?.path || 'root'; // removed an error here by adding second '?'
      });
  }
}
