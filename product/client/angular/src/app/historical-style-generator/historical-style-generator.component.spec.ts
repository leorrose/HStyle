import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HistoricalStyleGeneratorComponent } from './historical-style-generator.component';

describe('HistoricalStyleGeneratorComponent', () => {
  let component: HistoricalStyleGeneratorComponent;
  let fixture: ComponentFixture<HistoricalStyleGeneratorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HistoricalStyleGeneratorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HistoricalStyleGeneratorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
