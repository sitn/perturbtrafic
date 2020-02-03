import { AfterViewInit, ChangeDetectorRef, Component, OnChanges, OnInit, SimpleChanges, Input, Output, EventEmitter } from '@angular/core';
import OlTileLayer from 'ol/layer/Tile';
import OlTileWMS from 'ol/source/TileWMS';
import OlMap from 'ol/Map';
import * as OlProj from 'ol/proj';
import { fromLonLat } from 'ol/proj';
import OlView from 'ol/View';
import { IPerturbationImpression } from 'src/app/models/perturbation/IPerturbation';
import { MapService } from 'src/app/services/map.service';
import { ConfigService } from 'src/app/services/config.service';

@Component({
  selector: 'impression-evenement',
  templateUrl: './impression-evenement.component.html',
  styleUrls: ['./impression-evenement.component.less']
})
export class ImpressionEvenementComponent implements OnInit, OnChanges, AfterViewInit {

  // evenementImpression: IEvenementImpression;
  @Input() perturbationImpression: IPerturbationImpression;
  @Output() perturbationRendered = new EventEmitter<boolean>();
  todayDate: Date;

  constructor(private ref: ChangeDetectorRef, private configService: ConfigService, private mapService: MapService) { }

  ngOnInit() {
    this.todayDate = new Date();

  }

  ngAfterViewInit() {
    this.initializeMap();
  }



  initializeMap() {

    const config = this.configService.getConfig();
    const wmsSource = new OlTileWMS({
      url: config.sitnWS.fond_plan.baseUrl,
      params: { 'LAYERS': config.sitnWS.fond_plan.layers.plan_cadastral, 'VERSION': config.sitnWS.fond_plan.version },
      crossOrigin: ''
    });
    const tileLayer = new OlTileLayer({
      source: wmsSource
    });

    const view = new OlView({
      // center: fromLonLat([6.931933, 46.992979]),
      center: OlProj.transform(fromLonLat([6.931933, 46.992979]), 'EPSG:3857', 'EPSG:2056'),
      projection: 'EPSG:2056',
      zoom: 12,
      maxZoom: 19
    });
    // this.perturbationsImpressions.forEach(pert => {
    const map = new OlMap({
      target: 'printMap_' + this.perturbationImpression.id,
      // target: 'superMap',
      layers: [tileLayer],
      view: view,
      id: this.perturbationImpression.id
    });
    this.mapService.addFeaturesToPrintMap(map,
      this.perturbationImpression.geometry_point, this.perturbationImpression.geometry_ligne,
      this.perturbationImpression.geometry_polygone);
    this.ref.detectChanges();


    let counter = 0;
    wmsSource.on('tileloadstart', () => {
      counter = counter + 1;
    });
    wmsSource.on('tileloaderror', () => {
      counter = counter - 1;
      if (counter === 0) {
        map.render();
      }
    });
    wmsSource.on('tileloadend', () => {
      counter = counter - 1;
      if (counter === 0) {
        map.render();
        map.once('rendercomplete', (event) => {
          const canvas = event.context.canvas;
          this.perturbationImpression.canvas = canvas.toDataURL();
          this.perturbationRendered.emit();
          this.ref.detectChanges();
        });
      }
    });

    map.renderSync();

    map.once('postrender', (event) => {
      this.ref.detectChanges();
    });
  }



  ngOnChanges(changes: SimpleChanges) {
  }

}
