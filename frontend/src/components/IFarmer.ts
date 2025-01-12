export interface ICulture {
    id?: number;
    name: string;
}

export interface ICrop {
    id: number;
    culture_id?: number;
    date: string;
    farm_id: number;
    culture?: ICulture;
    culture_name?: string;
}

export interface IFarm {
    id: number;
    vegetation_area: number;
    farmer_id: number;
    state: string;
    name: string;
    arable_area: number;
    total_area: number;
    city: string;
    crops?: ICrop[];
}

export default interface IFarmer {
    state: string;
    name: string;
    city: string;
    id: number;
    document: string;
    farms?: IFarm[];
}