import { Component, HostListener, OnInit } from '@angular/core';
import OlTileLayer from 'ol/layer/Tile';
import OlMap from 'ol/Map';
import { fromLonLat } from 'ol/proj';
import OlSourceOSM from 'ol/source/osm';
import OlSourceBingMaps from 'ol/source/bingmaps';
import OlView from 'ol/View';
import * as OlProj from 'ol/proj';
import { EvenementFormService } from 'src/app/services/evenement-form.service';
import { MapService } from 'src/app/services/map.service';

@Component({
  selector: 'carte-evenement',
  templateUrl: './carte-evenement.component.html',
  styleUrls: ['./carte-evenement.component.less']
})
export class CarteEvenementComponent implements OnInit {

  isSnappingMode = false;
  public map: OlMap;

  layer: OlTileLayer;
  view: OlView;

  constructor(private mapService: MapService, public evenementFormService: EvenementFormService) {
  }

  ngOnInit() {


    this.view = new OlView({
      // center: fromLonLat([6.931933, 46.992979]),
      center: OlProj.transform(fromLonLat([6.931933, 46.992979]), 'EPSG:3857', 'EPSG:2056'),
      projection: 'EPSG:2056',
      zoom: 12,
      maxZoom: 19
    });

    this.map = new OlMap({
      target: 'map',
      layers: [],
      view: this.view
    });

    this.mapService.setMap(this.map, 'EVENEMENT');
  }

}
