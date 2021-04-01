import { TestBed } from '@angular/core/testing';

import { DemoService } from './demo.service';

describe('DemoService', () => {
    let service: DemoService;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(DemoService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should return DemoImagesPaths object', () => {
        const demoImagesPaths = service.getDemoImagesPaths();
        expect(demoImagesPaths.contentImage).toEqual('assets/hstyle_demo/content.webp');
        expect(demoImagesPaths.styleImage).toEqual('assets/hstyle_demo/style.webp');
        expect(demoImagesPaths.resultImage).toEqual('assets/hstyle_demo/result.webp');
    });
});
