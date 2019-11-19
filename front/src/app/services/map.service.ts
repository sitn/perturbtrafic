import { EventEmitter, Injectable, OnInit } from '@angular/core';
import * as OlCondition from 'ol/events/condition';
import * as OlExtent from 'ol/extent';
import OlFeature from 'ol/Feature';
import OlFormatGeoJSON from 'ol/format/geojson';
import OlDraw from 'ol/interaction/Draw';
import OlModify from 'ol/interaction/Modify';
import OlInteractionMouseWheelZoom from 'ol/interaction/MouseWheelZoom';
import OlInteractionDblClick from 'ol/interaction/DoubleClickZoom';
import Select from 'ol/interaction/Select';
import OlInteractionSnap from 'ol/interaction/Snap';
import OlLayerVector from 'ol/layer/Vector';
import { bbox as bboxStrategy } from 'ol/loadingstrategy';
import OlMap from 'ol/Map';
import { register } from 'ol/proj/proj4.js';
import OlSourceVector from 'ol/source/Vector';
import OlImageLayer from 'ol/layer/Image';
import OlTileWMS from 'ol/source/TileWMS';
import OlTileLayer from 'ol/layer/Tile';
import OlStyleCircle from 'ol/style/Circle';
import OlStyleFill from 'ol/style/Fill';
import OlStyleStroke from 'ol/style/Stroke';
import OlStyleStyle from 'ol/style/Style';
import proj4 from 'proj4';

import { IContact } from '../models/IContact';
import { IOrganisme } from '../models/IOrganisme';
import { ReperageGridLine, ReperageServerForSave } from '../models/IReperage';
import { LoaderService } from '../core/loader/loader.service';
import { ConfigService } from './config.service';
import { IConfig } from '../models/IConfig';

@Injectable()
export class MapService implements OnInit {

    config: IConfig;

    evenementPrintMap: OlMap;
    perturbationsPrintMap: OlMap[];

    map: OlMap;
    currentDrawInteraction: OlDraw;
    currentDeviationDrawInteraction: OlDraw;
    drawSource: any;
    drawVector: any;
    deviationDrawSource: any;
    deviationDrawVector: any;

    axesNationauxSnapping: any;
    axesCantonauxSnapping: any;
    axesCommunauxSnapping: any;

    axesNationauxVectorSource: any;
    axesNationauxVector: any;
    axesCantonauxVectorSource: any;
    axesCantonauxVector: any;
    axesCommunauxVectorSource: any;
    axesCommunauxVector: any;
    selectSingleClick: Select;
    modifyInteraction: OlModify;

    public contactReceived$: EventEmitter<IContact[]>;
    public organismesReceived$: EventEmitter<IOrganisme[]>;
    public featureWithReperageIdRemoved$: EventEmitter<{ id_reperage: number }>;
    public printMapRendered$: EventEmitter<any>;
    public currentDrawType;
    public currentFormType;
    public isFeatureSelected = false;
    public isEditing = false;
    public isDeviation = false;
    public isSnapping = false;
    public previousFeatureGeometryEdition;

    private printRenderCounter = 0;

    constructor(private loaderService: LoaderService, private configService: ConfigService) {

        this.isDeviation = false;
        this.featureWithReperageIdRemoved$ = new EventEmitter();
        this.printRenderCounter = 0;
        this.printMapRendered$ = new EventEmitter();
        proj4.defs('EPSG:2056', `+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +
        k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs`);
        /* proj4.defs('EPSG:2056', `+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +
        k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs`); */
        register(proj4);
        this.drawSource = new OlSourceVector({ wrapX: false });
        this.drawVector = new OlLayerVector({
            source: this.drawSource,
            name: 'draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 0, 0, 1.0)',
                    width: 3
                })
            }),
            zIndex: 999
        });

        this.deviationDrawSource = new OlSourceVector({ wrapX: false });
        this.deviationDrawVector = new OlLayerVector({
            source: this.deviationDrawSource,
            name: 'deviation_draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 0, 0, 1.0)',
                    width: 3
                })
            }),
            zIndex: 999
        });

        this.selectSingleClick = new Select({
            wrapX: false,
            condition: function (evt) {
                return false;
            }
        });
        this.modifyInteraction = new OlModify({
            features: this.selectSingleClick.getFeatures()
        });

        this.config = this.configService.getConfig();
        this.perturbationsPrintMap = [];
    }

    ngOnInit() {
    }

    setPrintMap(map: OlMap) {
        /* this.printMap = map;
        this.printMap.addLayer(this.drawVector); */
    }

    addFeaturesToPrintMap(map: OlMap, geometry_point: any, geometry_ligne: any, geometry_polygone: any): void {
        let geometries = [];
        if (geometry_point && geometry_point.length > 0) {
            geometries = geometries.concat(geometry_point);
        }
        if (geometry_ligne && geometry_ligne.length > 0) {
            geometries = geometries.concat(geometry_ligne);
        }
        if (geometry_polygone && geometry_polygone.length > 0) {
            geometries = geometries.concat(geometry_polygone);
        }
        const drawSource = new OlSourceVector({ wrapX: false });
        const drawVector = new OlLayerVector({
            source: drawSource,
            name: 'draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 0, 0, 1.0)',
                    width: 3
                }),
                image: new OlStyleCircle({
                    radius: 5,
                    fill: new OlStyleFill({
                        color: 'rgba(255, 0, 0, 1.0)'
                    }),
                    stroke: new OlStyleStroke({
                        color: 'rgba(0, 0, 255, 1.0)'
                    })
                })
            }),
            zIndex: 999
        });

        const deviationDrawSource = new OlSourceVector({ wrapX: false });
        const deviationDrawVector = new OlLayerVector({
            source: deviationDrawSource,
            name: 'deviation_draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 0, 0, 1.0)',
                    width: 3
                })
            }),
            zIndex: 999
        });

        if (geometries && geometries.length > 0) {
            let extent = OlExtent.createEmpty();
            geometries.forEach((geometry, index) => {
                const olGeometry = (new OlFormatGeoJSON()).readGeometry(geometry);
                const id_rep = geometry.id_reperage;
                let feature;
                if (id_rep) {
                    feature = new OlFeature({
                        geometry: olGeometry,
                        id: geometry.id,
                        id_reperage: id_rep
                    });
                } else {
                    feature = new OlFeature({
                        geometry: olGeometry,
                        id: geometry.id
                    });
                }
                drawVector.getSource().addFeature(feature);
                if (index === 0) {
                    extent = olGeometry.getExtent();
                } else {
                    extent = OlExtent.extend(extent, olGeometry.getExtent());
                }
            });
            map.addLayer(drawVector);
            map.addLayer(deviationDrawVector);
            map.getView().fit(extent);

        }

    }

    /*     onPrintRenderStart() {
            if (this.printRenderCounter === 0) {
                this.loaderService.show();
            }
            this.printRenderCounter = this.printRenderCounter + 1;

        } */

    onPrintRenderFinish() {
        this.printRenderCounter = this.printRenderCounter - 1;
        if (this.printRenderCounter === 0) {
            this.loaderService.hide();
        }
    }

    setMap(map: OlMap, formType: string) {
        console.log('set map ');
        this.isDeviation = false;
        this.currentFormType = formType;
        this.drawSource = new OlSourceVector({ wrapX: false });
        this.drawVector = new OlLayerVector({
            source: this.drawSource,
            name: 'draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 0, 0, 1.0)',
                    width: 4
                }),
                image: new OlStyleCircle({
                    radius: 5,
                    fill: new OlStyleFill({
                        color: 'rgba(255, 0, 0, 1.0)'
                    }),
                    stroke: new OlStyleStroke({
                        color: 'rgba(0, 0, 255, 1.0)'
                    })
                })
            }),
            zIndex: 999
        });
        const fondCartoWMSSource = new OlTileWMS({
            url: this.config.sitnWS.fond_plan.baseUrl,
            params: {
                'LAYERS': this.config.sitnWS.fond_plan.layers.plan_cadastral,
                'VERSION': this.config.sitnWS.fond_plan.version,
            },
            crossOrigin: null
        });
        const tileLayer = new OlTileLayer({
            source: fondCartoWMSSource
        });
        const wmsLayers = this.config.sitnWS.wms.layers;
        const routesWMSSource = new OlTileWMS({
            url: this.config.sitnWS.wms.baseUrl,
            params: {
                'LAYERS': wmsLayers.axes_nationaux + ',' + wmsLayers.secteurs_nationaux + ',' + wmsLayers.axes_communaux
                    + ',' + wmsLayers.secteurs_communaux + ',' + wmsLayers.axes_cantonaux + ',' + wmsLayers.secteurs_cantonaux
                    + ',' + wmsLayers.hectometrage,
                'VERSION': this.config.sitnWS.wms.version
            },
            crossOrigin: null
        });
        const routesTileLayer = new OlTileLayer({
            source: routesWMSSource
        });

        this.deviationDrawSource = new OlSourceVector({ wrapX: false });
        this.deviationDrawVector = new OlLayerVector({
            source: this.deviationDrawSource,
            name: 'deviation_draw_layer',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(255, 255, 20, 1.0)',
                    width: 4
                }),
                image: new OlStyleCircle({
                    radius: 5,
                    fill: new OlStyleFill({
                        color: 'rgba(255, 0, 0, 1.0)'
                    }),
                    stroke: new OlStyleStroke({
                        color: 'rgba(0, 0, 255, 1.0)'
                    })
                })
            }),
            zIndex: 999
        });
        this.map = map;
        this.axesNationauxVectorSource = new OlSourceVector({
            format: new OlFormatGeoJSON(),
            url: (extent) => {
                return this.config.sitnWS.wfs.baseUrl + '?service=WFS&version=' + this.config.sitnWS.wfs.version +
                    '&request=GetFeature&typename=' + this.config.sitnWS.wfs.layers.axes_nationaux
                    + '&outputformat=geojson&bbox=' + extent.join(',') +
                    'urn:ogc:def:crs:EPSG:2056';
            },
            strategy: bboxStrategy
        });

        this.axesNationauxVector = new OlLayerVector({
            source: this.axesNationauxVectorSource,
            name: 'axesNationaux',
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(119, 136, 153, 1.0)',
                    width: 2
                })
            })
        });


        this.axesCantonauxVectorSource = new OlSourceVector({
            format: new OlFormatGeoJSON(),
            url: (extent) => {
                return this.config.sitnWS.wfs.baseUrl + '?service=WFS&version=' + this.config.sitnWS.wfs.version +
                    '&request=GetFeature&typename=' + this.config.sitnWS.wfs.layers.axes_cantonaux
                    + '&outputformat=geojson&bbox=' + extent.join(',') +
                    'urn:ogc:def:crs:EPSG:2056';
            },
            strategy: bboxStrategy
        });

        this.axesCantonauxVector = new OlLayerVector({
            name: 'axesCantonaux',
            source: this.axesCantonauxVectorSource,
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(119, 136, 153, 0)',
                    width: 1
                })
            })
        });
        this.axesCommunauxVectorSource = new OlSourceVector({
            format: new OlFormatGeoJSON(),
            url: (extent) => {
                return this.config.sitnWS.wfs.baseUrl + '?service=WFS&version=' + this.config.sitnWS.wfs.version +
                    '&request=GetFeature&typename=' + this.config.sitnWS.wfs.layers.axes_communaux
                    + '&outputformat=geojson&bbox=' + extent.join(',') +
                    'urn:ogc:def:crs:EPSG:2056';
            },
            strategy: bboxStrategy
        });
        this.axesCommunauxVector = new OlLayerVector({
            name: 'axesCommunaux',
            source: this.axesCommunauxVectorSource,
            style: new OlStyleStyle({
                stroke: new OlStyleStroke({
                    color: 'rgba(119, 136, 153, 0)',
                    width: 1
                })
            })
        });
        this.map.addLayer(this.drawVector);
        this.map.addLayer(this.deviationDrawVector);
        this.map.addLayer(this.axesNationauxVector);
        this.map.addLayer(tileLayer);
        this.map.addLayer(routesTileLayer);
        this.map.addLayer(this.axesCantonauxVector);
        // Remove MouseWheelZoomInteraction
        const zoomInteractionIndex = this.map.getInteractions().getArray().findIndex(inter => {
            if (inter instanceof OlInteractionMouseWheelZoom) {
                return true;
            }
        });
        if (zoomInteractionIndex > -1) {
            this.map.getInteractions().getArray().splice(zoomInteractionIndex, 1);
        }

        // Remove DblClickInteraction
        const dblClickInteractionIndex = this.map.getInteractions().getArray().findIndex(inter => {
            if (inter instanceof OlInteractionDblClick) {
                return true;
            }
        });
        if (dblClickInteractionIndex > -1) {
            this.map.getInteractions().getArray().splice(dblClickInteractionIndex, 1);
        }

        const mouseWheelInt = new OlInteractionMouseWheelZoom();
        this.map.addInteraction(mouseWheelInt);
        this.map.on('wheel', evt => {
            mouseWheelInt.setActive(OlCondition.shiftKeyOnly(evt));
        });
        this.map.on('moveend', evt => {
            const axesCommunauxLayer = this.findLayerByName('axesCommunaux');
            if (evt.map.getView().getZoom() > 13) {
                if (!axesCommunauxLayer) {
                    this.map.addLayer(this.axesCommunauxVector);
                }
            } else {
                if (axesCommunauxLayer) {
                    this.map.removeLayer(this.axesCommunauxVector);
                }
            }
        });
        this.addSelectSingleClickInteraction();
        console.log('end set map with extent : ', this.map.getView().calculateExtent());

    }

    addSnapping() {
        this.isSnapping = true;
        const axesCantonauxLayer = this.findLayerByName('axesCantonaux');
        const axesCommunauxLayer = this.findLayerByName('axesCommunaux');
        const axesNationauxLayer = this.findLayerByName('axesNationaux');
        if (axesCantonauxLayer) {
            this.axesCantonauxSnapping = new OlInteractionSnap({
                source: axesCantonauxLayer.getSource()
            });
            this.map.addInteraction(this.axesCantonauxSnapping);
        }
        if (axesNationauxLayer) {
            this.axesNationauxSnapping = new OlInteractionSnap({
                source: axesNationauxLayer.getSource()
            });
            this.map.addInteraction(this.axesNationauxSnapping);
        }
        if (axesCommunauxLayer) {
            this.axesCommunauxSnapping = new OlInteractionSnap({
                source: axesCommunauxLayer.getSource()
            });
            this.map.addInteraction(this.axesCommunauxSnapping);
        }
    }

    removeSnapping() {
        this.isSnapping = false;
        this.map.removeInteraction(this.axesNationauxSnapping);
        this.map.removeInteraction(this.axesCantonauxSnapping);
        this.map.removeInteraction(this.axesCommunauxSnapping);
        this.axesNationauxSnapping = null;
        this.axesCantonauxSnapping = null;
        this.axesCommunauxSnapping = null;
    }


    toggleSnapping() {
        if (this.isSnapping) {
            this.removeSnapping();
        } else {
            this.addSnapping();
        }
    }

    startDrawing(type: string) {
        this.removeAllInteraction();
        this.addDrawInteraction(type);
        this.currentDrawType = type;
    }

    startDeviationDrawing() {
        this.removeAllInteraction();
        this.addDeviationDrawInteraction();
        this.currentDrawType = 'Deviation';
    }

    cancelCurrentDraw() {
        this.removeSnapping();
        this.map.removeInteraction(this.currentDrawInteraction);
        this.map.removeInteraction(this.currentDeviationDrawInteraction);
        this.addSelectSingleClickInteraction();
        this.currentDrawType = null;
    }

    setDeviation(isDeviation: boolean) {
        this.isDeviation = isDeviation;
    }

    initializeFeaturesAndExtent(geometries: any[]): void {
        if (geometries && geometries.length > 0) {
            geometries.forEach((geometry, index) => {
                const olGeometry = (new OlFormatGeoJSON()).readGeometry(geometry.geometry);
                const id_rep = geometry.id_reperage;
                let feature;
                if (id_rep) {
                    feature = new OlFeature({
                        geometry: olGeometry,
                        id: geometry.id,
                        id_reperage: id_rep
                    });
                } else {
                    feature = new OlFeature({
                        geometry: olGeometry,
                        id: geometry.id
                    });
                }
                this.getDrawLayer().getSource().addFeature(feature);
            });
            const extent = this.calculateExtent();
            setTimeout(() => {
                this.map.getView().fit(extent);
                this.map.render();
            }, 200);
        }
    }

    initializeDeviationsAndExtent(deviations: any[]): void {
        if (deviations && deviations.length > 0) {
            deviations.forEach((geometry, index) => {
                const olGeometry = (new OlFormatGeoJSON()).readGeometry(geometry.geometry);
                let feature;
                feature = new OlFeature({
                    geometry: olGeometry,
                    id: geometry.id
                });
                this.getDeviationDrawLayer().getSource().addFeature(feature);
            });
            const extent = this.calculateExtent();
            setTimeout(() => {
                this.map.getView().fit(extent);
                this.map.render();
            }, 1000);
        }
    }

    calculateExtent(): any {
        let extent = OlExtent.createEmpty();
        this.getDrawLayer().getSource().getFeatures().forEach((feature, index) => {
            if (index === 0) {
                extent = feature.getGeometry().getExtent();
            } else {
                extent = OlExtent.extend(extent, feature.getGeometry().getExtent());
            }
        });
        this.getDeviationDrawLayer().getSource().getFeatures().forEach((feature, index) => {
            if (index === 0) {
                extent = feature.getGeometry().getExtent();
            } else {
                extent = OlExtent.extend(extent, feature.getGeometry().getExtent());
            }
        });
        extent = OlExtent.buffer(extent, 10);
        return extent;
    }

    setPrintMapExtent() {
        // this.printMap.getView().fit(this.calculateExtent());
    }

    removeFeature() {
        console.log(this.selectSingleClick);
        if (this.selectSingleClick && this.selectSingleClick.getFeatures()) {
            const features = this.selectSingleClick.getFeatures();
            features.forEach(feature => {
                this.getDrawLayer().getSource().removeFeature(feature);
                if (feature.get('id_reperage')) {
                    this.featureWithReperageIdRemoved$.emit({ id_reperage: feature.get('id_reperage') });
                }
            });
            this.selectSingleClick.getFeatures().clear();
            this.isEditing = false;
            this.isFeatureSelected = false;
        }
    }



    updateFeatures(geomReperages: any[], deletedReperages: number[]) {
        const olFeatures = [];
        if (deletedReperages && deletedReperages.length > 0) {
            deletedReperages.forEach(rep_id => {
                this.getDrawLayer().getSource().getFeatures().forEach(feature => {
                    const geomReperageId = feature.get('id_reperage');
                    if (geomReperageId && geomReperageId === rep_id) {
                        this.getDrawLayer().getSource().removeFeature(feature);
                    }
                });
            });
        }
        geomReperages.forEach((geomReperage: any) => {
            if (geomReperage) {
                const olGeometry = (new OlFormatGeoJSON()).readGeometry(geomReperage);
                const olFeature = new OlFeature({
                    geometry: olGeometry,
                    id_reperage: geomReperage.id
                });
                olFeatures.push(olFeature);
            }
        });

        if (olFeatures.length > 0) {
            this.getDrawLayer().getSource().addFeatures(olFeatures);
        }
        const extent = this.calculateExtent();
        if (!OlExtent.isEmpty(extent)) {
            this.map.getView().fit(extent);
        }
    }

    editFeature() {
        if (this.isEditing) {
            this.map.removeInteraction(this.modifyInteraction);
            this.selectSingleClick.getFeatures().clear();
            this.isEditing = false;
        } else if (this.selectSingleClick.getFeatures().getLength() > 0) {
            console.log('add modify interaction', this.modifyInteraction);
            this.isEditing = true;
            this.previousFeatureGeometryEdition = this.selectSingleClick.getFeatures().getArray()[0].clone().getGeometry();
            this.addModifyInteraction();
        }
    }

    cancelCurrentEdition() {
        this.isSnapping = false;
        this.map.removeInteraction(this.modifyInteraction);
        const currentFeatureEdition = (this.getDrawLayer().getSource().getFeatures() as any[]).find(feature => {
            return feature.ol_uid === this.selectSingleClick.getFeatures().getArray()[0].ol_uid;
        });
        if (currentFeatureEdition) {
            currentFeatureEdition.setGeometry(this.previousFeatureGeometryEdition);
        }
        this.previousFeatureGeometryEdition = null;
        this.selectSingleClick.getFeatures().clear();
        this.isFeatureSelected = false;
        this.isEditing = false;
    }


    onDrawEnd(evt) {
        this.isSnapping = false;
        this.removeAllInteraction();
        this.addSelectSingleClickInteraction();
        this.currentDrawType = null;
    }

    removeAllInteraction() {
        this.map.removeInteraction(this.selectSingleClick);
        this.map.removeInteraction(this.modifyInteraction);
        this.map.removeInteraction(this.currentDrawInteraction);
        this.map.removeInteraction(this.currentDeviationDrawInteraction);
    }

    getIsEditingValue(): boolean {
        return !this.isEditing;
    }

    addSelectSingleClickInteraction() {
        this.selectSingleClick = new Select({
            /* filter: (e) => {
                if (this.isEditing) {
                    return false;
                } else {
                    return true;
                }
                // return !this.isEditing && this.selectSingleClick.getFeatures().getLength() < 1;
            }, */
            condition: (e) => {
                if (e.type === 'singleclick') {
                    if (!this.isEditing) {
                        return true;
                    } else {
                        return false;
                    }
                } else {
                    return false;
                }
            },
            // toggleCondition: (OlCondition.never),
            toggleCondition: () => {
                return false;
                /* if (!this.isEditing) {
                    return false;
                } else {
                    return !this.isEditing; // && this.selectSingleClick.getFeatures().getLength() < 1;
                } */
                // return this.isEditing && this.selectSingleClick.getFeatures().getLength() > 0;
            }
            /* filter: (e) => {
                return !this.isEditing;
            } */
        });
        this.selectSingleClick.on('select', e => {
            if (this.selectSingleClick.getFeatures().getLength() > 0) {
                this.isFeatureSelected = true;
            } else {
                this.isFeatureSelected = false;
            }
            if (!this.currentDrawType) {

            }
            if (this.isEditing) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
            if (e.target.getFeatures().getLength() > 0) {
                if (!this.currentDrawType) {

                }
                console.log('feature selected');
            } else {
                console.log('feature selected');
            }
        });
        this.selectSingleClick.on('change', e => {
            console.log('selection changed');
            if (this.isEditing) {
                console.log('do not unselect');
            }
        });
        this.map.addInteraction(this.selectSingleClick);
    }

    addModifyInteraction() {
        this.map.removeInteraction(this.modifyInteraction);
        this.modifyInteraction = new OlModify({
            features: this.selectSingleClick.getFeatures()
        });
        this.map.addInteraction(this.modifyInteraction);
    }

    addDrawInteraction(type: string) {
        this.currentDrawInteraction = new OlDraw({
            source: this.getDrawLayer().getSource(),
            type: type
        });
        this.map.addInteraction(this.currentDrawInteraction);
        this.currentDrawInteraction.on('drawend', evt => {
            this.onDrawEnd(evt);
        });
    }

    addDeviationDrawInteraction() {
        this.currentDeviationDrawInteraction = new OlDraw({
            source: this.getDeviationDrawLayer().getSource(),
            type: 'LineString'
        });
        this.map.addInteraction(this.currentDeviationDrawInteraction);
        this.currentDeviationDrawInteraction.on('drawend', evt => {
            this.onDrawEnd(evt);
        });
    }

    getListOfFeatures(): any {
        console.log(this.drawSource);
        this.prepareFeaturesForSaving();
    }

    findLayerByName(layerName: string): any {
        let foundLayer;
        this.map.getLayers().forEach(layer => {
            if (layer.get('name') === layerName) {
                foundLayer = layer;
            }
        });
        return foundLayer;
    }

    getDrawLayer(): any {
        return this.findLayerByName('draw_layer');
    }

    getDeviationDrawLayer(): any {
        return this.findLayerByName('deviation_draw_layer');
    }

    prepareFeaturesForSaving(reperages?: ReperageGridLine[]): any[] {
        /* const pointFeatures: any[] = [];
        const lineFeatures: any[] = [];
        const polygonFeatures: any[] = []; */
        const features: any[] = [];
        this.getDrawLayer().getSource().getFeatures().forEach(feature => {
            const shape = JSON.parse((new OlFormatGeoJSON()).writeFeature(feature)).geometry;
            const geomReperageId = feature.get('id_reperage');
            let reperage;
            if (geomReperageId && reperages && reperages.length > 0) {
                reperage = reperages.find(rep => {
                    return rep.id === geomReperageId;
                });
            }
            /* if (shape.type === 'Point') {
                features.push(shape);
            } else if (shape.type === 'LineString') {
                lineFeatures.push(shape);
            } else if (shape.type === 'Polygon') {
                polygonFeatures.push(shape);
            } */
            if (reperage) {
                features.push({ geometry: shape, reperage: new ReperageServerForSave(reperage) });
            } else {
                features.push({ geometry: shape });
            }
            console.log(shape);
        });

        /* const features = {
            points: pointFeatures,
            lines: lineFeatures,
            polygons: polygonFeatures
        }; */
        return features;
    }

    prepareDeviationsFeaturesForSaving(): any[] {
        const features: any[] = [];
        this.getDeviationDrawLayer().getSource().getFeatures().forEach(feature => {
            const shape = JSON.parse((new OlFormatGeoJSON()).writeFeature(feature)).geometry;

            features.push(shape);
            console.log(shape);
        });

        return features;
    }
}
