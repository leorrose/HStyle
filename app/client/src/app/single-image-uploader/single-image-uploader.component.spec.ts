import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleImageUploaderComponent } from './single-image-uploader.component';

describe('SingleImageUploaderComponent', () => {
    let component: SingleImageUploaderComponent;
    let fixture: ComponentFixture<SingleImageUploaderComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [
                SingleImageUploaderComponent,
            ],
            schemas: [NO_ERRORS_SCHEMA]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(SingleImageUploaderComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
