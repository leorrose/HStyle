export interface StyleTransferRequest {
    email: string;
    styleLoss: number;
    contentLoss: number;
    totalVariationLoss: number;
    contentImage: File;
    styleImage: File;
    applyDilation: boolean;
}
