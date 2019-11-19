import { Component, OnInit, HostListener } from '@angular/core';
import OlTileLayer from 'ol/layer/Tile';
import OlMap from 'ol/Map';
import { fromLonLat } from 'ol/proj';
import OlSourceOSM from 'ol/source/osm';
import OlSourceBingMaps from 'ol/source/bingmaps';
import OlView from 'ol/View';
import * as OlProj from 'ol/proj';
import { MapService } from 'src/app/services/map.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';

@Component({
  selector: 'carte-perturbation',
  templateUrl: './carte-perturbation.component.html',
  styleUrls: ['./carte-perturbation.component.less']
})
export class CartePerturbationComponent implements OnInit {


  public map: OlMap;

  view: OlView;

  constructor(private mapService: MapService, public perturbationFormService: PerturbationFormService) {
  }

  ngOnInit() {
    /* this.layer = new OlTileLayer({
      source: new OlSourceOSM(),
      name: 'base_osm'
    }); */

    this.view = new OlView({
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

    this.mapService.setMap(this.map, 'PERTURBATION');
  }
}
