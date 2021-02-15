export interface StyleTransferRequest {
  styleLoss: number;
  contentLoss: number;
  totalVariationLoss: number;
  contentImage: File;
  styleImage: File;
  applyDilation: boolean;
}
