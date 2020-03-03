export interface IConfig {
    version: string;
    wsPath: string;
    urlGuichetCarto: string;
    wsSitnBaseUrl: string;
    sitnWS: {
        fond_plan: {
            baseUrl: string;
            version: string;
            layers: {
                plan_cadastral: string;
            }
        };
        wms: {
            baseUrl: string;
            version: string;
            layers: {
                axes_nationaux: string;
                secteurs_nationaux: string;
                axes_cantonaux: string;
                secteurs_cantonaux: string;
                hectometrage: string;
                secteurs_communaux: string;
                axes_communaux: string;
            }
        };
        wfs: {
            baseUrl: string;
            version: string;
            layers: {
                axes_nationaux: string;
                axes_cantonaux: string;
                axes_communaux: string;
            }
        }
    };
    mapStyle: {
        deviation: {
            color: string;
            contour: string;
            contourWidth: number;
            width: number;
        },
        perturbation: {
            color: string;
            contour: string;
            contourWidth: number;
            width: number;
        }
    };
    listeSuggestions: {
        occupation: string;
        voieCondamnee: string;
        division: string;
        regulationPar: string;
    };
    evenementPerturbationFieldsMapping: {
        geometries: string;
        description: string;
        date_debut: string;
        date_fin: string;
        heure_debut: string;
        heure_fin: string;
        localisation: string;
    };
}
