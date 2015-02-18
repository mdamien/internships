class InternshipsController < ApplicationController
before_action :set_internship, only: [:show]

  #GET /internships/id.json
  def show

  end

  def set_internship
    @internship = Internship.find(params[:id])
  end

end
