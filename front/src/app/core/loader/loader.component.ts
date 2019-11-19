import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoaderService } from './loader.service';

@Component({
  selector: 'app-ui-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.less']
})
export class LoaderComponent implements OnInit, OnDestroy {

  visible = false;

  private subscription: Subscription;

  constructor(private loaderService: LoaderService, private ref: ChangeDetectorRef) { }

  ngOnInit() {
    this.subscription = this.loaderService.loaderState
      .subscribe((state: boolean) => {
        this.visible = state;
        this.ref.detectChanges();
      });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }
}
