import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnChanges, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import OlTileLayer from 'ol/layer/Tile';
import OlMap from 'ol/Map';
import * as OlProj from 'ol/proj';
import OlSourceBingMaps from 'ol/source/bingmaps';
import OlView from 'ol/View';
import OlTileWMS from 'ol/source/TileWMS';
import { IPerturbationImpression } from 'src/app/models/perturbation/IPerturbation';
import { ApiService } from 'src/app/services/api.service';
import { PerturbationFormService } from 'src/app/services/perturbation-form.service';
import { fromLonLat } from 'ol/proj';
import { MapService } from 'src/app/services/map.service';
import { PDFComponent } from '@progress/kendo-angular-grid';
import { LoaderService } from 'src/app/core/loader/loader.service';
import { exportPDF } from '@progress/kendo-drawing';
import { saveAs } from '@progress/kendo-file-saver';
import { ConfigService } from 'src/app/services/config.service';

@Component({
  selector: 'impression-perturbation',
  templateUrl: './impression-perturbation.component.html',
  styleUrls: ['./impression-perturbation.component.less'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ImpressionPerturbationComponent implements OnInit, OnChanges, AfterViewInit {

  perturbationImpression: IPerturbationImpression;

  todayDate: Date;

  constructor(public perturbationFormService: PerturbationFormService, private route: ActivatedRoute, private apiService: ApiService,
    private ref: ChangeDetectorRef, private mapService: MapService,
    private loaderService: LoaderService, private configService: ConfigService) {

  }

  ngOnInit() {
    this.todayDate = new Date();
    const perturbationId = this.route.snapshot.paramMap.get('id');
    if (perturbationId) {
      this.apiService.getPerturbationImpression(perturbationId).subscribe(pertImpression => {
        this.perturbationImpression = pertImpression;
        this.initializeMap();
        this.ref.detectChanges();
      });
    }
  }

  ngOnChanges() {
  }

  ngAfterViewInit() {
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
    const map = new OlMap({
      target: 'map',
      layers: [tileLayer],
      view: view
    });
    this.mapService.addFeaturesToPrintMap(map,
      this.perturbationImpression.geometry_point, this.perturbationImpression.geometry_ligne,
      this.perturbationImpression.geometry_polygone, this.perturbationImpression.geometry_deviation);
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
          this.ref.detectChanges();
        });
      }
    });

    map.renderSync();

    map.once('postrender', (event) => {
      this.ref.detectChanges();
    });
  }

  printPerturbation(pdf: PDFComponent): void {
    this.loaderService.show(true);
    pdf.export().then(val => {
      return exportPDF(val, { paperSize: 'A4' });
    }).then(dataUri => {
      saveAs(dataUri, 'Evenements.pdf');
      this.loaderService.hide(true);
    });
  }

}
