import { StyleTransferRequest } from './../models/style-transfer-request';
import { environment } from './../../environments/environment';
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestApiService {

  constructor(private http: HttpClient) { }

  test(data:StyleTransferRequest): Promise<string> {
    let formData = new FormData();
    formData.append('content_image', data.contentImage);
    formData.append('style_image', data.styleImage);

    let url = environment.API_URL + '/styleTransfer/renderImage'
    url += `?content_loss=${data.contentLoss}`
    url += `&style_loss=${data.styleLoss}`
    url += `&total_variation_loss=${data.totalVariationLoss}`
    url += `&apply_dilation=${data.applyDilation}`


    return this.http.post(url, formData).toPromise().then(
      (res:string) => {
        return res;
      },
      (err: HttpErrorResponse) => {
        console.log(err);
        return '';
      }
    );
  }
}
