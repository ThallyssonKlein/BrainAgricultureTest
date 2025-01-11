export interface IStateFarmCount {
    state: string;
    farm_count: number;
}

export interface ICultureFarmCount {
    culture: string;
    farm_count: number;
}

export interface IAverageLandUse {
    average_arable_area: number;
    average_vegetation_area: number;
}

export interface IData {
    farm_count: number;
    total_hectares: number;
    farm_counts_grouped_by_state: IStateFarmCount[];
    farms_count_grouped_by_culture: ICultureFarmCount[];
    average_land_use: IAverageLandUse;
}