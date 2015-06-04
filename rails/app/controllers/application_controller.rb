class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
  before_filter :set_search_query, :only => [:index]

  before_filter CASClient::Frameworks::Rails::Filter

  def index
    @all_filieres_grouped_by_branches = Internship.all_filieres
    @all_levels = Internship.all_levels_for_select
    @all_branches = Internship.all_branches_for_select

    # Retrieving most recent year data from database by default.
    @internships = Internship.search(params).order_internships_for_table
    @internships_geolocalized = @internships.map {
        |i| {
          company: i.company,
          subject: i.subject,
          address: i.address,
          latitude: i.latitude,
          longitude: i.longitude,
          id: i.id,
          url: url_for(controller: 'application', action: 'view', id: i.id)
      }
    }

    # Internship data values in JSON (countries, cities, companies).
    # These Sets are used so store autocomplete values in the table.
    @internship_data_json = {
        "countries" => SortedSet.new,
        "cities" => SortedSet.new,
        "companies" => SortedSet.new
    }

    # Filling sets with data.
    @internships.each do |i|
      @internship_data_json["countries"].add(i.country.titleize) unless i.country.nil?
      @internship_data_json["cities"].add(i.city.titleize) unless i.city.nil?
      @internship_data_json["companies"].add(i.company.titleize) unless i.company.nil?
    end
  end

  # View of a single internship when clicking on it in the table/map.
  def view
    @internship = Internship.find(params[:id])
  end

  def logout
    CASClient::Frameworks::Rails::Filter.logout(self)
  end

  protected

  # Default search parameters.
  def set_search_query
    @all_semesters = Internship.all_semesters_ordered

    # Adding missing parameters by default.
    params[:from_semester] ||= @all_semesters.size > 1 ? @all_semesters[1] : @all_semesters.first()
    params[:to_semester] ||= @all_semesters.first()
  end
end