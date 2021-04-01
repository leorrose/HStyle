import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule} from '@angular/common/http/testing';
import { HistoricalStyleGeneratorComponent } from './historical-style-generator.component';
import { RestApiService } from '../services/rest-api.service';

describe('HistoricalStyleGeneratorComponent', () => {
    let component: HistoricalStyleGeneratorComponent;
    let fixture: ComponentFixture<HistoricalStyleGeneratorComponent>;
    let RestApiServiceMock = jasmine.createSpyObj('RestApiService', ['generateImage']);

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [HistoricalStyleGeneratorComponent],
            providers: [
                { provide: RestApiService, useValue: RestApiServiceMock}
            ],
            imports: [ HttpClientTestingModule ]
        }).compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(HistoricalStyleGeneratorComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should set content image', () => {
        let test_file = new File([""], "filename", { type: 'text/html' });
        component.setContentImage(test_file);
        expect(component.contentImage).toEqual(test_file);
    });

    it('should set style image', () => {
        let test_file = new File([""], "filename", { type: 'text/html' });
        component.setStyleImage(test_file);
        expect(component.styleImage).toEqual(test_file);
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
        let email = component.inputs.controls['email'];
        expect(email.valid).toBeFalsy();

        email.setValue("");
        expect(email.hasError('required')).toBeTruthy();

        email.setValue("test");
        expect(email.hasError('pattern')).toBeTruthy();

        email.setValue("test@gmail.com");
        expect(email.valid).toBeTruthy();
    });

    it('styleLoss field validity', () => {
        let styleLoss = component.inputs.controls['styleLoss'];
        expect(styleLoss.valid).toBeTruthy();
        expect(styleLoss.value).toEqual(0.01);

        styleLoss.setValue("");
        expect(styleLoss.hasError('required')).toBeTruthy();

        styleLoss.setValue(0.2);
        expect(styleLoss.hasError('max')).toBeTruthy();

        styleLoss.setValue(-0.1);
        expect(styleLoss.hasError('min')).toBeTruthy();

        styleLoss.setValue(0.01);
        expect(styleLoss.valid).toBeTruthy();
    });

    it('contentLoss field validity', () => {
        let contentLoss = component.inputs.controls['contentLoss'];
        expect(contentLoss.valid).toBeTruthy();
        expect(contentLoss.value).toEqual(150);

        contentLoss.setValue("");
        expect(contentLoss.hasError('required')).toBeTruthy();

        contentLoss.setValue(100001);
        expect(contentLoss.hasError('max')).toBeTruthy();

        contentLoss.setValue(9);
        expect(contentLoss.hasError('min')).toBeTruthy();

        contentLoss.setValue(1500);
        expect(contentLoss.valid).toBeTruthy();
    });

    it('totalVariationLoss field validity', () => {
        let totalVariationLoss = component.inputs.controls['totalVariationLoss'];
        expect(totalVariationLoss.valid).toBeTruthy();
        expect(totalVariationLoss.value).toEqual(30);

        totalVariationLoss.setValue("");
        expect(totalVariationLoss.hasError('required')).toBeTruthy();

        totalVariationLoss.setValue(31);
        expect(totalVariationLoss.hasError('max')).toBeTruthy();

        totalVariationLoss.setValue(29);
        expect(totalVariationLoss.hasError('min')).toBeTruthy();

        totalVariationLoss.setValue(30);
        expect(totalVariationLoss.valid).toBeTruthy();
    });

    it('should generate image with good response', (done) => {
        let email = component.inputs.controls['email']
        email.setValue("test@test.com");
        let styleLoss = component.inputs.controls['styleLoss']
        styleLoss.setValue(0.01);
        let contentLoss = component.inputs.controls['contentLoss']
        contentLoss.setValue(150);
        let totalVariationLoss = component.inputs.controls['totalVariationLoss']
        totalVariationLoss.setValue(30);
        RestApiServiceMock.generateImage.and.returnValue(true);


        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).toHaveBeenCalled();
            expect(component.generateImageMessage).toContain('The process will');
            expect(email.value).toEqual("");
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
        let email = component.inputs.controls['email']
        email.setValue("test@test.com");
        let styleLoss = component.inputs.controls['styleLoss']
        styleLoss.setValue(0.01);
        let contentLoss = component.inputs.controls['contentLoss']
        contentLoss.setValue(150);
        let totalVariationLoss = component.inputs.controls['totalVariationLoss']
        totalVariationLoss.setValue(30);
        RestApiServiceMock.generateImage.and.returnValue(false);


        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).toHaveBeenCalled();
            expect(component.generateImageMessage).toContain('A problem occurred');
            expect(email.value).toEqual("");
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
        let email = component.inputs.controls['email']
        email.setValue("");
        component.generateImage().then(() => {
            expect(RestApiServiceMock.generateImage).not.toHaveBeenCalled();
            done();
        })
        .catch(err => {
          fail(err);
        });
    });
});
