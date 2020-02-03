import { Component, OnInit, ChangeDetectorRef, AfterViewInit } from '@angular/core';
import { IEvenementImpression } from 'src/app/models/evenement/IEvenement';
import { IPerturbationImpression } from 'src/app/models/perturbation/IPerturbation';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { MapService } from 'src/app/services/map.service';
import { LoaderService } from 'src/app/core/loader/loader.service';
import OlTileLayer from 'ol/layer/Tile';
import OlTileWMS from 'ol/source/TileWMS';
import OlMap from 'ol/Map';
import * as OlProj from 'ol/proj';
import { fromLonLat } from 'ol/proj';
import OlSourceBingMaps from 'ol/source/bingmaps';
import OlView from 'ol/View';
import { Group, exportPDF } from '@progress/kendo-drawing';
import { saveAs } from '@progress/kendo-file-saver';
import { PDFComponent } from '@progress/kendo-angular-grid';
import { ConfigService } from 'src/app/services/config.service';

@Component({
  selector: 'impression-evenement-container',
  templateUrl: './impression-evenement-container.component.html',
  styleUrls: ['./impression-evenement-container.component.less']
})
export class ImpressionEvenementContainerComponent implements OnInit, AfterViewInit {

  evenementImpression: IEvenementImpression;
  perturbationsImpressions: IPerturbationImpression[];

  perturbationsRenderedCounter = 0;

  todayDate: Date;

  constructor(private route: ActivatedRoute, private apiService: ApiService, private ref: ChangeDetectorRef,
    private loaderService: LoaderService, private mapService: MapService, private configService: ConfigService) { }

  ngOnInit() {

    this.todayDate = new Date();
    this.perturbationsRenderedCounter = 0;
    const evenementId = this.route.snapshot.paramMap.get('id');
    if (evenementId) {
      const printPath = this.route.snapshot.url.findIndex(url => url.path.toLowerCase() === 'print'.toLowerCase());
      const printFolderPath = this.route.snapshot.url.findIndex(url => url.path.toLowerCase() === 'print_folder'.toLowerCase());
      if (printPath > -1) {
        this.apiService.getEvenementImpression(evenementId).subscribe(eveImpression => {
          this.evenementImpression = eveImpression;
          this.renderEvenementMap();
        });
      } else if (printFolderPath > -1) {
        this.apiService.getDossierEvenementImpression(evenementId).subscribe(dossierImpression => {
          this.loaderService.show(true);
          this.evenementImpression = dossierImpression.evenement;
          this.perturbationsImpressions = dossierImpression.perturbations;
          this.ref.detectChanges();
          this.renderEvenementMap();

        });
      }
    }
  }

  renderEvenementMap(): void {
    const config = this.configService.getConfig();
    this.loaderService.show(true);

    const wmsSource = new OlTileWMS({
      url: config.sitnWS.fond_plan.baseUrl,
      params: { 'LAYERS': config.sitnWS.fond_plan.layers.plan_cadastral, 'VERSION': config.sitnWS.fond_plan.version },
      crossOrigin: ''
    });
    const tileLayer = new OlTileLayer({
      source: wmsSource
    });

    const view = new OlView({
      center: OlProj.transform(fromLonLat([6.931933, 46.992979]), 'EPSG:3857', 'EPSG:2056'),
      projection: 'EPSG:2056',
      zoom: 12,
      maxZoom: 19
    });
    const map = new OlMap({
      target: 'evenementPrintMap',
      layers: [tileLayer],
      view: view
    });
    this.mapService.addFeaturesToPrintMap(map,
      this.evenementImpression.geometry_point, this.evenementImpression.geometry_ligne,
      this.evenementImpression.geometry_polygone);
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
          this.evenementImpression.canvas = canvas.toDataURL();
          this.loaderService.hide(true);
          this.ref.detectChanges();
        });
      }
    });

    map.renderSync();

    map.once('postrender', (event) => {
      this.ref.detectChanges();
    });
  }

  onPerturbationMapRendered() {
    this.perturbationsRenderedCounter = this.perturbationsRenderedCounter + 1;
    if (this.perturbationsImpressions.length === this.perturbationsRenderedCounter) {
      this.loaderService.hide(true);
    }
  }

  ngAfterViewInit() {
  }

  printEvenement(pdf: PDFComponent): void {
    this.loaderService.show(true);

    pdf.export().then(val => {
      return exportPDF(val, { paperSize: 'A4' });
    }).then(dataUri => {
      saveAs(dataUri, 'Evenements.pdf');
      this.loaderService.hide(true);
    });
  }

}
