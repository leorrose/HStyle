import { SingleImageUploaderComponent } from './../single-image-uploader/single-image-uploader.component';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule} from '@angular/common/http/testing';
import { HistoricalStyleGeneratorComponent } from './historical-style-generator.component';
import { RestApiService } from '../services/rest-api.service';
import { NO_ERRORS_SCHEMA } from '@angular/core';

describe('HistoricalStyleGeneratorComponent', () => {
    let component: HistoricalStyleGeneratorComponent;
    let fixture: ComponentFixture<HistoricalStyleGeneratorComponent>;
    const RestApiServiceMock = jasmine.createSpyObj('RestApiService', ['generateImage']);

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [
                HistoricalStyleGeneratorComponent
            ],
            providers: [
                { provide: RestApiService, useValue: RestApiServiceMock}
            ],
            imports: [ HttpClientTestingModule ],
            schemas: [NO_ERRORS_SCHEMA]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(HistoricalStyleGeneratorComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    afterEach(() => {
        RestApiServiceMock.generateImage.calls.reset();

    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should set content image', () => {
        const testFile = new File([''], 'filename', { type: 'text/html' });
        component.setContentImage(testFile);
        expect(component.contentImage).toEqual(testFile);
    });

    it('should set style image', () => {
        const testFile = new File([''], 'filename', { type: 'text/html' });
        component.setStyleImage(testFile);
        expect(component.styleImage).toEqual(testFile);
    });

    it('should toggle dilation from true to false', () => {
        component.addDilation = true;
        component.toggleDilation();
        expect(component.addDilation).toEqual(false);
    });

    it('should toggle dilation from false to true', () => {
        component.addDilation = false;
        component.toggleDilation();
        expect(component.addDilation).toEqual(true);
    });

    it('form invalid when empty', () => {
        expect(component.inputs.valid).toBeFalsy();
    });

    it('email field validity', () => {
        const email = component.inputs.get('email');
        expect(email.valid).toBeFalsy();

        email.setValue('');
        expect(email.hasError('required')).toBeTruthy();

        email.setValue('test');
        expect(email.hasError('pattern')).toBeTruthy();

        email.setValue('test@gmail.com');
        expect(email.valid).toBeTruthy();
    });

    it('styleLoss field validity', () => {
        const styleLoss = component.inputs.get('styleLoss');
        expect(styleLoss.valid).toBeTruthy();
        expect(styleLoss.value).toEqual(0.01);

        styleLoss.setValue('');
        expect(styleLoss.hasError('required')).toBeTruthy();

        styleLoss.setValue(0.2);
        expect(styleLoss.hasError('max')).toBeTruthy();

        styleLoss.setValue(-0.1);
        expect(styleLoss.hasError('min')).toBeTruthy();

        styleLoss.setValue(0.01);
        expect(styleLoss.valid).toBeTruthy();
    });

    it('contentLoss field validity', () => {
        const contentLoss = component.inputs.get('contentLoss');
        expect(contentLoss.valid).toBeTruthy();
        expect(contentLoss.value).toEqual(150);

        contentLoss.setValue('');
        expect(contentLoss.hasError('required')).toBeTruthy();

        contentLoss.setValue(100001);
        expect(contentLoss.hasError('max')).toBeTruthy();

        contentLoss.setValue(9);
        expect(contentLoss.hasError('min')).toBeTruthy();

        contentLoss.setValue(1500);
        expect(contentLoss.valid).toBeTruthy();
    });

    it('totalVariationLoss field validity', () => {
        const totalVariationLoss = component.inputs.get('totalVariationLoss');
        expect(totalVariationLoss.valid).toBeTruthy();
        expect(totalVariationLoss.value).toEqual(30);

        totalVariationLoss.setValue('');
        expect(totalVariationLoss.hasError('required')).toBeTruthy();

        totalVariationLoss.setValue(31);
        expect(totalVariationLoss.hasError('max')).toBeTruthy();

        totalVariationLoss.setValue(29);
        expect(totalVariationLoss.hasError('min')).toBeTruthy();

        totalVariationLoss.setValue(30);
        expect(totalVariationLoss.valid).toBeTruthy();
    });

    it('should generate image with good response', (done) => {
        const email = component.inputs.get('email');
        email.setValue('test@test.com');
        const styleLoss = component.inputs.get('styleLoss');
        styleLoss.setValue(0.01);
        const contentLoss = component.inputs.get('contentLoss');
        contentLoss.setValue(150);
        const totalVariationLoss = component.inputs.get('totalVariationLoss');
        totalVariationLoss.setValue(30);
        RestApiServiceMock.generateImage.and.returnValue(true);


        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).toHaveBeenCalled();
            expect(component.generateImageMessage).toContain('The process will');
            expect(email.value).toEqual('');
            expect(styleLoss.value).toEqual(0.01);
            expect(contentLoss.value).toEqual(150);
            expect(totalVariationLoss.value).toEqual(30);
            done();
        })
        .catch(err => {
          fail(err);
        });
    });

    it('should generate image with bad response', (done) => {
        const email = component.inputs.get('email');
        email.setValue('test@test.com');
        const styleLoss = component.inputs.get('styleLoss');
        styleLoss.setValue(0.01);
        const contentLoss = component.inputs.get('contentLoss');
        contentLoss.setValue(150);
        const totalVariationLoss = component.inputs.get('totalVariationLoss');
        totalVariationLoss.setValue(30);
        RestApiServiceMock.generateImage.and.returnValue(false);


        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).toHaveBeenCalled();
            expect(component.generateImageMessage).toContain('A problem occurred');
            expect(email.value).toEqual('');
            expect(styleLoss.value).toEqual(0.01);
            expect(contentLoss.value).toEqual(150);
            expect(totalVariationLoss.value).toEqual(30);
            done();
        })
        .catch(err => {
          fail(err);
        });
    });

    it('should not generate image', (done) => {
        expect(component.inputs.valid).toBeFalsy();
        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).not.toHaveBeenCalled();
            done();
        })
        .catch(err => {
          fail(err);
        });
    });
});
