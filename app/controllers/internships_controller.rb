class InternshipsController < ApplicationController
before_action :set_internship, only: [:show]

  #GET /internships/id.json
  def show

  end

  def search_internships

    if !params[:search_by].blank? and !params[:q].blank?
      if !["company", "country", "city"].include? params[:search_by]
        return
      else

      end
    else
      return
    end

    @data = Internship.
        select(params[:search_by]).
        where(params[:search_by] + " LIKE ?", "%" + params[:q] + "%")
        .distinct
        .limit(8)
        .order(params[:search_by] + " ASC")
        .map { |c| c[params[:search_by]] }
  end

  def set_internship
    @internship = Internship.find(params[:id])
  end

end