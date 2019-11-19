import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModeEmploiComponent } from './mode-emploi.component';

describe('ModeEmploiComponent', () => {
  let component: ModeEmploiComponent;
  let fixture: ComponentFixture<ModeEmploiComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModeEmploiComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModeEmploiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
