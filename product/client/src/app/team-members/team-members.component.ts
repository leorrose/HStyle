import { TeamMemberService } from '../services/team-member.service';
import { TeamMember } from './../models/team-member';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-team-members',
  templateUrl: './team-members.component.html',
  styleUrls: ['./team-members.component.css']
})
export class TeamMembersComponent implements OnInit {
  teamMembers: Array<TeamMember[]>;

  constructor(private teamMemberService: TeamMemberService) { }

  ngOnInit(): void {
    this.teamMembers = this.chunkArray(this.teamMemberService.getTeamMembers(), 3);
  }

  chunkArray(array: TeamMember[] , size: number): Array<TeamMember[]> {
    const result = [];
    const arrayCopy = [...array];
    while (arrayCopy.length > 0) {
        result.push(arrayCopy.splice(0, size));
    }

    if (result[result.length - 1].length !== size){
      const toAdd = size - result[result.length - 1].length;
      for (let i = 0 ; i < toAdd; i++){
        result[result.length - 1].push({});
      }
    }
    return result;
  }
}
