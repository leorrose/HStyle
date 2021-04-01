import { TestBed } from '@angular/core/testing';

import { TeamMemberService } from './team-member.service';

describe('TeamMemberServiceService', () => {
    let service: TeamMemberService;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(TeamMemberService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    it('should return team member array', () => {
        const teamMembers = service.getTeamMembers();
        expect(teamMembers.length).toEqual(3);
    });
});
