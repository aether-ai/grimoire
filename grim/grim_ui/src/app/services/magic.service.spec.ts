import { TestBed } from '@angular/core/testing';

import { MagicService } from './magic.service';

describe('MagicService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MagicService = TestBed.get(MagicService);
    expect(service).toBeTruthy();
  });
});
