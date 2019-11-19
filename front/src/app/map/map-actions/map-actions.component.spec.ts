import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MapActionsComponent } from './map-actions.component';

describe('MapActionsComponent', () => {
  let component: MapActionsComponent;
  let fixture: ComponentFixture<MapActionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MapActionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MapActionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
