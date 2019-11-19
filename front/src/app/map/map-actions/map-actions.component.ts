import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MapService } from 'src/app/services/map.service';
import { NavigationService } from 'src/app/services/navigation.service';

@Component({
  selector: 'map-actions',
  templateUrl: './map-actions.component.html',
  styleUrls: ['./map-actions.component.less']
})
export class MapActionsComponent implements OnInit {

  crudMode: string;

  constructor(public mapService: MapService, private route: ActivatedRoute, private navigationService: NavigationService) {
    this.crudMode = 'READ_ONLY';
  }

  ngOnInit() {
    const editPath = this.route.snapshot.url.findIndex(url => url.path === 'edit');
    const viewPath = this.route.snapshot.url.findIndex(url => url.path === 'view');
    if (viewPath > -1) {
      this.crudMode = 'READ_ONLY';
    } else if (editPath > -1) {
      this.crudMode = 'EDIT';
    } else {
      this.crudMode = 'NEW';
    }
  }


  startNewDraw(type: string) {
    this.mapService.startDrawing(type);
  }

  startDeviationDraw() {
    this.mapService.startDeviationDrawing();
  }

  editFeature() {
    this.mapService.editFeature();
  }

  removeFeature() {
    this.mapService.removeFeature();
  }

  cancelCurrentDraw() {
    this.mapService.cancelCurrentDraw();
  }

  cancelCurrentEdition() {
    this.mapService.cancelCurrentEdition();
  }

  editReperage() {
    this.navigationService.openSaisieReperageDialog();
  }

  toggleSnapping() {
    this.mapService.toggleSnapping();
  }

}
