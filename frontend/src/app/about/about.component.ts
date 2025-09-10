import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { SlackInviteBox } from '../navigation/widgets/slack-invite-box/slack-invite-box.widget';
import { Subscription } from 'rxjs';

@Component({
    selector: 'app-about',
    templateUrl: './about.component.html',
    standalone: false
})
export class AboutComponent implements OnInit, OnDestroy {
  private socket$: WebSocketSubject<any>;
  private socketSubscription?: Subscription;

  public static Route = {
    path: 'about',
    title: 'About the XL',
    component: AboutComponent
  };

  constructor(protected dialog: MatDialog) {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const url = `${protocol}://${window.location.host}/ws/echo`;
    this.socket$ = webSocket({ url });
  }

  ngOnInit(): void {
    let counter = 0;
    this.socketSubscription = this.socket$.subscribe((message) => {
      console.log(`Received: ${message}`);
      setTimeout(() => this.socket$.next(`counter: ${counter++}`), 1000);
    });
    this.socket$.next('onInit');
  }

  ngOnDestroy(): void {
    this.socketSubscription?.unsubscribe();
  }

  onSlackInviteClick(): void {
    const dialogRef = this.dialog.open(SlackInviteBox, {
      width: '1000px',
      autoFocus: false
    });
    dialogRef.afterClosed().subscribe();
  }
}
